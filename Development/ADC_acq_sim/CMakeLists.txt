cmake_minimum_required(VERSION 3.12)

# Include build functions from Pico SDK
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
include($ENV{PICO_SDK_PATH}/tools/CMakeLists.txt)
include_directories(${PROJECT_SOURCE_DIR})

# Set name of project (as PROJECT_NAME) and C/C++ standards
project(ADC_acq_sim C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)


# Creates a pico-sdk subdirectory in our project for the libraries
pico_sdk_init()

# Tell CMake where to find the executable source file
add_executable(  
    ${PROJECT_NAME}
)

# Create C header file with the name <pio program>.pio.h
pico_generate_pio_header(${PROJECT_NAME}  
        ${CMAKE_CURRENT_LIST_DIR}/ADC_acq_sim.pio
)

target_sources(${PROJECT_NAME} PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/ADC_acq_sim.c

)

 # Make sure TinyUSB can find tusb_config.h
 target_include_directories(${PROJECT_NAME} PUBLIC
 ${CMAKE_CURRENT_LIST_DIR})

 # Create map/bin/hex/uf2 files
pico_add_extra_outputs(${PROJECT_NAME})

target_link_libraries(${PROJECT_NAME} 
        pico_stdlib
        hardware_pwm  
        hardware_clocks
        hardware_pio
        hardware_i2c
)