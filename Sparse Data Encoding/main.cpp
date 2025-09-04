// Enables the decoding of sparse data given a certain input
// Uncomment the include and pthread functions if pthread.h is defined
// Also comment MakeRow in the pthread loop

//#include <pthread.h>
#include <iostream>
#include <string>
#include <vector>

// To store a symbol and its ranges
struct symbolAndRanges {
    char symbol;
    std::vector<int*>* ranges;
    symbolAndRanges(std::vector<int*>* rainges = new std::vector<int*>(), char c = ' ') {
        symbol = c;
        ranges = rainges;
    }
    ~symbolAndRanges() {
        delete ranges;
    }
};

// Stores all the information needed for the pthread function in a structure
struct Info {
    int rowNum;
    char* line;
    std::vector<symbolAndRanges*> bigList;
    std::vector<int> headPos;
    std::vector<int> dataPos;
    Info(int rowNumber, char* lin, std::vector<symbolAndRanges*>& largeList, std::vector<int>& headArray, std::vector<int>& dataArray) {
        rowNum = rowNumber;
        line = lin;
        bigList = largeList;
        headPos = headArray;
        dataPos = dataArray;
    }
};

void GetInfo(std::vector<symbolAndRanges*>& bigList, std::string line);
void FillVector(std::vector<int>& list, std::string line);
char FindSymbol(std::vector<symbolAndRanges*>& list, int xPos);
bool IsInRange(std::vector<int*>& ranges, int num);
void* MakeRow(void* infoPtr);
void PrintPicture(char** picture, int length, int width);

int main() {
    int length, width;
    // They are static because they are shared between multiple threads
    static std::vector<int> headPos;
    static std::vector<int> dataPos;
    static std::vector<symbolAndRanges*> bigList;
    std::string temp{};

    // First line of input
    std::cin >> length >> width;
    getline(std::cin, temp);

    // Makes empty 2d array of characters
    char** picture = new char* [width];
    for (int row = 0; row < width; row++) {
        picture[row] = new char[length];
        for (int col = 0; col < length; col++) {
            picture[row][col] = ' ';
        }
    }

    /*  Second line of input should contain at least two characters. 
        Each character should be followed by at least two numbers all seperated by spaces representing ranges.
        These numbers come in pairs and are bounded by the length given earlier.
        Each character-number sequence is seperated by a single comma.  */
    getline(std::cin, temp);
    // Loads second line into a vector of symbolAndRanges
    GetInfo(bigList, temp);

    // Third line is the input for the headPos vector
    // The headPos vector indexes into the dataPos vector and holds the index of the first entry in each row
    getline(std::cin, temp);
    FillVector(headPos, temp);

    // Input for the dataPos vector
    // Holds the x-positon of each non-whitespace character from left to right and top to bottom
    getline(std::cin, temp);
    FillVector(dataPos, temp);

    //pthread_t* tid = new pthread_t[width];
    for (int row = 0; row < width; row++) {
        Info* info = new Info(row, picture[row], bigList, headPos, dataPos);
        // If using pthread library comment false and uncomment pthread_create
        if (/*pthread_create(&tid[row], nullptr, MakeRow, info) != 0*/ false) {
            std::cerr << "Error creating thread" << std::endl;
            return 1;
        }
        // Comment if using pthread library
        MakeRow( (void*) info);
    }
    
    for (int row = 0; row < width; row++) {
        //pthread_join(tid[row], nullptr);
    }

    PrintPicture(picture, length, width);

    for (int row = 0; row < width; row++) {
        delete[] picture[row];
    }
    delete[] picture;

    return 0;
}

// Reads the second line of input
void GetInfo(std::vector<symbolAndRanges*>& bigList, std::string line) {
    const int arraySize = 2;
    char symbol;
    std::string temp = line, symbolInfo{};
    std::vector<int*> ranges;

    // Split at first comma
    int cut = temp.find(',');
    int firstNum, secondNum, smallCut;
    while (cut != -1) {
        // One symbol-range sequence
        symbolInfo = temp.substr(0, cut);
        // Everything else
        temp = temp.substr(cut + 1);
        // Find next comma if one exists
        cut = temp.find(',');

        // Symbol is first character followed by a space and the range(s)
        symbol = symbolInfo[0];
        smallCut = symbolInfo.find(' ');

        while (smallCut != -1) {
            // Get next pair and remove space
            symbolInfo = symbolInfo.substr(smallCut + 1);
            // Find next space
            smallCut = symbolInfo.find(' ');
            firstNum = stoi(symbolInfo.substr(0, smallCut));

            symbolInfo = symbolInfo.substr(smallCut + 1);
            secondNum = stoi(symbolInfo);
            ranges.push_back(new int[arraySize] {firstNum, secondNum});
            smallCut = symbolInfo.find(' ');
        }

        // ranges is copied into a new vector and then cleared because we cannot use the same vector for each set of ranges
        bigList.push_back(new symbolAndRanges(new std::vector<int*>(ranges), symbol));
        ranges.clear();
    }

    // Last symbol
    symbolInfo = temp;
    symbol = symbolInfo[0];
    smallCut = symbolInfo.find(' ');
    // Formatting for while loop
    symbolInfo = symbolInfo.substr(smallCut);

    // In case of trailing whitespace
    while (symbolInfo.length() >= 4) {
        // Remove the extra space and find the next one
        symbolInfo = symbolInfo.substr(1);
        smallCut = symbolInfo.find(' ');
        firstNum = stoi(symbolInfo.substr(0, smallCut));

        symbolInfo = symbolInfo.substr(smallCut + 1);
        secondNum = stoi(symbolInfo);
        ranges.push_back(new int[arraySize] {firstNum, secondNum});

        // This needs to come before the call to substr
        smallCut = symbolInfo.find(' ');
        if (smallCut == -1) {
            break;
        }
        // Formatting for while loop
        symbolInfo = symbolInfo.substr(smallCut);
    }

    bigList.push_back(new symbolAndRanges(new std::vector<int*>(ranges), symbol));
}

// Fills headPos or dataPos
void FillVector(std::vector<int>& list, std::string line) {
    int cut = line.find(' ');
    int num = stoi(line);
    list.push_back(num);
    // Formatting for while loop
    line = line.substr(cut);

    // In case of trailing whitespace
    while (line.length() >= 2) {
        line = line.substr(1);
        num = stoi(line);
        list.push_back(num);

        // Since we do not want to call substr with -1
        cut = line.find(' ');
        if (cut == -1) {
            break;
        }
        line = line.substr(cut);
    }
}

// Determines which symbol should be at xPos which is a column
char FindSymbol(std::vector<symbolAndRanges*>& list, int xPos) {
    for (int i = 0; i < list.size(); i++) {
        // The symbolAndRanges are pointers as this gives greater control over when they are deleted
        if (IsInRange(*list[i]->ranges, xPos)) {
            return list[i]->symbol;
        }
    }
    return ' ';
}

// Returns true if num is in at least one of a symbol's ranges, false otherwise
bool IsInRange(std::vector<int*>& ranges, int num) {
    for (int i = 0; i < ranges.size(); i++) {
        if (num >= ranges[i][0] && num <= ranges[i][1]) {
            return true;
        }
    }
    return false;
}

// Thread function needs to be of type void* and return a void*
void* MakeRow(void* infoVoidPtr) {
    // We need to cast to Info* befroe we can start accessing elements
    Info* infoPtr = (Info*)infoVoidPtr;
    const int rowNum = infoPtr->rowNum;
    int dataIndex = infoPtr->headPos[rowNum];
    int endIndex;
    // Last row case
    if (rowNum + 1 == infoPtr->headPos.size()) {
        endIndex = infoPtr->dataPos.size();
    }
    // We want to start at the current head index and end before the next head index
    else {
        endIndex = infoPtr->headPos[rowNum + 1];
    }

    while (dataIndex != endIndex) {
        int xPos = infoPtr->dataPos[dataIndex];
        char symbol;
        symbol = FindSymbol(infoPtr->bigList, xPos);
        infoPtr->line[xPos] = symbol;

        dataIndex++;
    }
    delete infoPtr;

    return nullptr;
}

void PrintPicture(char** picture, int length, int width) {
    for (int row = 0; row < width; row++) {
        for (int col = 0; col < length; col++) {
            std::cout << picture[row][col];
        }
        std::cout << std::endl;
    }
}