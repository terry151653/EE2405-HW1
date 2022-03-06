#include "mbed.h"
//3 but in. up, down, select. 1 when push
DigitalIn bntUp(D2);
DigitalIn bntSelect(D1);
DigitalIn bntDown(D0);
//1 analog out
AnalogOut aOut(D7);
//2 analog in
AnalogIn aIn1(D12);
AnalogIn aIn2(D11);
//ADC data (before and after)
float ADCdata1[1000] = {0};
float ADCdata2[1000] = {0};

int main()
{
    
    //select without loop
    int selectedFreq = 5;
    aOut = 0.4;
    //loop until select
    while (!bntSelect)
    {
        if (bntUp)
            selectedFreq += 1;
        if (bntDown && selectedFreq > 1)
            selectedFreq -= 1;
        
        printf("selected frequency: %d Hz\n", selectedFreq);
        do
        {
            ThisThread::sleep_for(10ms);
        }
        while (bntUp || bntDown);

        
        while (!bntSelect && !bntUp && !bntDown)
            ThisThread::sleep_for(10ms);
        
    }
    printf("Start\n");

    //r0 = 0.1, r1 = 0.5, Fcotoff = 8hz;
    int step1 = 1000 / selectedFreq, step2 = 1000 / (selectedFreq * 10), step3 = 500 / selectedFreq, revise = 200 % selectedFreq;

    for (int i = 0, k = 0; i < 1000; ++i, ++k)
    {
        if (k >= step1 + (revise > 0))
        {
            k = 0;
            --revise;
        }
        
        if (k < step2)
            aOut = (float)k / step2;
        else if (k > step3)
            aOut = 2 - (float)k / step3;
        else
            aOut = 1.0;

        ADCdata1[i] = aIn1;
        ADCdata2[i] = aIn2;

        ThisThread::sleep_for(1ms);
    }

    for (int i = 0; i < 1000; ++i)
    {
        printf("%f\r\n", ADCdata1[i]);
        //ThisThread::sleep_for(50ms);
    }
    
    for (int i = 0; i < 1000; ++i)
    {
        printf("%f\r\n", ADCdata2[i]);
        //ThisThread::sleep_for(50ms);
    }
    
}