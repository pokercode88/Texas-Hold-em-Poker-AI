cmake_minimum_required(VERSION 3.14)
project(TexasHoldemAI VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 设置编译选项
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang|AppleClang")
    add_compile_options(-Wall -Wextra -Wpedantic -O3)
endif()

# 查找依赖
find_package(Threads REQUIRED)
find_package(Python3 COMPONENTS Development REQUIRED)

# 包含目录
include_directories(${CMAKE_SOURCE_DIR}/src)

# 源文件列表（根据实际文件调整）
file(GLOB SOURCES
    "src/core/*.cpp"
    "src/env/*.cpp"
    "src/algorithms/*.cpp"
)

file(GLOB HEADERS
    "src/core/*.hpp"
    "src/env/*.hpp"
    "src/algorithms/*.hpp"
)

# 创建主库
add_library(holdem_core STATIC ${SOURCES} ${HEADERS})
target_link_libraries(holdem_core Threads::Threads ${Python3_LIBRARIES})

# 可执行文件示例
add_executable(run_main main.cpp)
target_link_libraries(run_main holdem_core)

# 测试（可选）
enable_testing()
add_executable(run_tests tests/test_core.cpp)
target_link_libraries(run_tests holdem_core)
add_test(NAME CoreTest COMMAND run_tests)

# 安装规则
install(TARGETS holdem_core run_main
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib/static
)