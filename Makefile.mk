CXX = g++
CXXFLAGS = -std=c++17 -O3 -Wall -Wextra
TARGET = holdem_ai
SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin

SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
OBJECTS = $(SOURCES:$(SRC_DIR)/%.cpp=$(OBJ_DIR)/%.o)

.PHONY: all clean run test

all: $(BIN_DIR)/$(TARGET)

$(BIN_DIR)/$(TARGET): $(OBJECTS) | $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $^ -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp | $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

run: $(BIN_DIR)/$(TARGET)
	./$(BIN_DIR)/$(TARGET)

test:
	python -m pytest tests/ -v

clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

format:
	black src/ tests/ scripts/
	clang-format -i $(SRC_DIR)/*.cpp $(SRC_DIR)/*.hpp