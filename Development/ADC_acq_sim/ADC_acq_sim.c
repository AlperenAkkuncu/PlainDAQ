/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

// Output PWM signals on pins 0 and 1

#define ADC_SDO 0
#define ADC_CNVST 1
#define ADC_SCLK 2
#define ADC_SDI 3
#define ADC_SDO_SIM 4

#define CLK_GEN_SM 0
#define GET_SAMPLE_SM 1
#define GEN_DATA_SM 2

#define IO_EXPANDER_ADDR 0x27
#define IODIR 0x00
#define IOPOL 0x01
#define OLAT 0x0A

#define CLK_FREQ 125000000
#define PWM_FREQ 500000

#include <stdio.h>
#include <math.h>
#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "hardware/clocks.h"
#include "hardware/pio.h"
#include "hardware/i2c.h"
#include "hardware/irq.h"
#include "ADC_acq_sim.pio.h"
#include "pico/binary_info.h"

uint16_t sample = 0;
uint32_t sample_tx_buff[4096], sample_rx_buff[4096];


void pio_sample_irq(){
    static uint32_t i = 0;
    irq_clear(PIO0_IRQ_0);
    if(i>4095){
        i = 0;
        sample_rx_buff[i] = pio_sm_get(pio0, GET_SAMPLE_SM);
        i++;
    }
    else{
        sample_rx_buff[i] = pio_sm_get(pio0, GET_SAMPLE_SM);
        i++;
    }
}

/*******************************************************************************
 * Function Declarations
 */
int reg_write(i2c_inst_t *i2c, 
                const uint addr, 
                const uint8_t reg, 
                uint8_t *buf,
                const uint8_t nbytes);

int reg_read(   i2c_inst_t *i2c,
                const uint addr,
                const uint8_t reg,
                uint8_t *buf,
                const uint8_t nbytes);

/*******************************************************************************
 * Function Definitions
 */

// Write 1 byte to the specified register
int reg_write(  i2c_inst_t *i2c, 
                const uint addr, 
                const uint8_t reg, 
                uint8_t *buf,
                const uint8_t nbytes) {

    int num_bytes_read = 0;
    uint8_t msg[nbytes + 1];

    // Check to make sure caller is sending 1 or more bytes
    if (nbytes < 1) {
        return 0;
    }

    // Append register address to front of data packet
    msg[0] = reg;
    for (int i = 0; i < nbytes; i++) {
        msg[i + 1] = buf[i];
    }

    // Write data to register(s) over I2C
    i2c_write_blocking(i2c, addr, msg, (nbytes + 1), false);

    return num_bytes_read;
}

// Read byte(s) from specified register. If nbytes > 1, read from consecutive
// registers.
int reg_read(  i2c_inst_t *i2c,
                const uint addr,
                const uint8_t reg,
                uint8_t *buf,
                const uint8_t nbytes) {

    int num_bytes_read = 0;

    // Check to make sure caller is asking for 1 or more bytes
    if (nbytes < 1) {
        return 0;
    }

    // Read data from register(s) over I2C
    i2c_write_blocking(i2c, addr, &reg, 1, true);
    num_bytes_read = i2c_read_blocking(i2c, addr, buf, nbytes, false);

    return num_bytes_read;
}

// I2C reserves some addresses for special purposes. We exclude these from the scan.
// These are any addresses of the form 000 0xxx or 111 1xxx
bool reserved_addr(uint8_t addr) {
    return (addr & 0x78) == 0 || (addr & 0x78) == 0x78;
}

void init_I2C(){
    i2c_init(i2c_default, 100 * 1000);
    gpio_set_function(8, GPIO_FUNC_I2C);
    gpio_set_function(9, GPIO_FUNC_I2C);
    gpio_pull_up(8);
    gpio_pull_up(9);
    // Make the I2C pins available to picotool
    bi_decl(bi_2pins_with_func(8, 9, GPIO_FUNC_I2C));
}

void set_channel_and_range(){
    uint8_t data;
    
    //setting channel one and range 1X
    //don't have much time to write a generic code...
    data = 0x5F;
    reg_write(i2c_default, IO_EXPANDER_ADDR, OLAT, &data,1);
    data = 0x00;
    reg_write(i2c_default, IO_EXPANDER_ADDR, IODIR, &data,1);
}

int main() {

       // Enable UART so we can print status output
    //stdio_init_all();

    /// \tag::ADC_SDI[]
    gpio_init(ADC_SDI);
    gpio_set_dir(ADC_SDI, GPIO_OUT);
    gpio_put(ADC_SDI, 1);
    /// \end::ADC_SDI[]
    
    /// \tag::i2c[]
    init_I2C();
    set_channel_and_range();
    /// \end::i2c[]

    /// \tag::pio[]
    // Choose PIO instance (0 or 1)
    PIO pio = pio0;
    PIO pio_1 = pio1;
    // Get first free state machine in PIO 0
    //uint sm_clk = pio_claim_unused_sm(pio, true);
    //uint sm_gen = pio_claim_unused_sm(pio_1, true);
    //uint sm_get_samples = pio_claim_unused_sm(pio, true);

    // Add PIO program to PIO instruction memory. SDK will find location and
    // return with the memory offset of the program.
    uint offset_clk = pio_add_program(pio0, &ADC_SCLK_gen_program);
    uint offset_gen = pio_add_program(pio0, &ADC_gen_sample_program);
    uint offset_get_sample = pio_add_program(pio0, &ADC_get_sample_program);

    // Initialize the program using the helper function in our .pio file
    ADC_SCLK_gen_init(pio0, CLK_GEN_SM, offset_clk, ADC_SCLK, 1);
    ADC_get_sample_init(pio0, GET_SAMPLE_SM, offset_get_sample,ADC_SDO_SIM);
    ADC_gen_sample_init(pio0, GEN_DATA_SM, offset_gen, ADC_SDO, 1);
    

    // Start running our PIO program in the state machine
    pio_sm_set_enabled(pio0, CLK_GEN_SM, true);
    pio_sm_set_enabled(pio0, GEN_DATA_SM, true);
    

    pio_set_irq0_source_enabled(pio0, pis_sm1_rx_fifo_not_empty, true);
    irq_set_exclusive_handler(PIO0_IRQ_0, &pio_sample_irq);
    irq_set_enabled(PIO0_IRQ_0, true);
    
    //pio0_hw->inte0 = PIO_IRQ0_INTE_SM0_BITS | PIO_IRQ0_INTE_SM1_BITS;
    /// \end::pio[]

    

    /// \tag::setup_pwm[]

    // Tell GPIO 0 and 1 they are allocated to the PWM
    //gpio_set_function(0, GPIO_FUNC_PWM);
    gpio_set_function(ADC_CNVST, GPIO_FUNC_PWM);

    // Find out which PWM slice is connected to GPIO 0 (it's slice 0)
    uint slice_num = pwm_gpio_to_slice_num(0);

    // Set period of 4 cycles (0 to 3 inclusive)
    pwm_set_wrap(slice_num, CLK_FREQ/PWM_FREQ );
    // Set initial B output high for three cycles before dropping
    // GPIO 1 is connected to PWM0B (datasheet page: 548)
    
    pwm_set_chan_level(slice_num, PWM_CHAN_B, 150);
    // Set the PWM running
    pwm_set_enabled(slice_num, true);
    /// \end::setup_pwm[]
    
    // Note we could also use pwm_set_gpio_level(gpio, x) which looks up the
    // correct slice and channel for a given GPIO.
    

    uint16_t i = sizeof(sample_tx_buff);
    
    for(i=0; i<( sizeof(sample_tx_buff)/4 ); i++){
        sample_tx_buff[i] = i;
        sample_rx_buff[i] = 0;
    }
        
    i = 0;

    pio_sm_set_enabled(pio0, GET_SAMPLE_SM, true);
    while(true){
                
        pio_sm_put_blocking(pio0, GEN_DATA_SM, (sample_tx_buff[i]<<20) );
        

        if( i >= (sizeof(sample_tx_buff)/4 - 1) )
            i = 0;
        else
            i++;

    }

}
