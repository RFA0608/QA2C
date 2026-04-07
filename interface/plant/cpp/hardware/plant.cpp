#define _USE_MATH_DEFINES
#include <iostream>
#include <cstdint>
#include <string>
#include <cmath>
#include <chrono>
#include "tcp_protocol_server_windows.h"
#include "hil.h"
#include "quanser_timer.h"
using namespace std;

const string host = "0.0.0.0";
const int port = 9999;

int main()
{
    t_card board;
    t_error result;
    // if you want to use hardware change to 1 else 0 is virtual(QLab)
    bool hardware = 0;

    if (hardware)
    {
        result = hil_open("quanser_aero2_usb", "0", &board);
        if (result < 0)
        {
            cout << "failure to connect hardware" << endl;
            return -1;
        }
    }
    else
    {
        result = hil_open("quanser_aero2_usb", "0@tcpip://localhost:18950", &board);
        if (result < 0)
        {
            cout << "failure to connect QLab" << endl;
            return -1;
        }
    }

    // simulation_time is total run time, sample_time is sample_time.
    int simulation_time = 30;
    double sample_time = 0.1;
    t_timeout interval;
    t_timeout timeout;
    timeout_get_timeout(&interval, sample_time);
    timeout_get_current_time(&timeout);

    double state[4] = { 0.0, 0.0, 0.0, 0.0 };
    double voltage[2] = { 0.0, 0.0 };
    double ref[2] = { 0.0, 0.0 };
    int32_t encoder_counts[4];
    uint32_t encoder_channels[4] = { 0, 1, 2, 3 };
    double other_counts[10];
    uint32_t other_channles[10] = { 3000, 3001, 3002, 4000, 4001, 4002, 14000, 14001, 14002, 14003 };
    uint32_t analog_channels[2] = { 0, 1 };
    uint32_t digital_channels[2] = { 0, 1 };
    t_boolean digital_values[2] = { 1, 1 };
    hil_write_digital(board, digital_channels, 2, digital_values);

    // calculation angle
    double theta_pitch = 0.0;
    double theta_yaw = 0.0;
    double rate_pitch = 0.0;
    double rate_yaw = 0.0;


    // TCP/IP ready
    tcp_server tcsp = tcp_server(host, port);

    // Just check loop/total time
    auto stc = chrono::high_resolution_clock::now();
    auto edc = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::nanoseconds>(edc - stc);
    double run_time = duration.count() / 1000000;
    double stack_time = 0.0;


    // control loop
    for (int64_t i = 0; i < (int64_t)((double)simulation_time / sample_time); i++)
    {
        stc = chrono::high_resolution_clock::now();

        // time sleep
        timeout_add(&timeout, &timeout, &interval);
        qtimer_sleep(&timeout);

        // read sensor
        hil_read_encoder(board, encoder_channels, 4, encoder_counts);
        hil_read_other(board, other_channles, 10, other_counts);
        theta_pitch =  encoder_counts[2] * (2.0 * M_PI / 2880);
        theta_yaw = encoder_counts[3] * (2.0 * M_PI / 4096);
        rate_pitch = other_counts[8] * (2.0 * M_PI / 2880);
        rate_yaw = other_counts[9] * (2.0 * M_PI / 4096);

        // running signal send for controller
        tcsp.Send<string>("run");

        // send plant output
        tcsp.Send<double>(theta_pitch);
        tcsp.Send<double>(theta_yaw);
        tcsp.Send<double>(rate_pitch);
        tcsp.Send<double>(rate_yaw);

        // get control input
        voltage[0] = tcsp.Recv<double>();
        voltage[1] = tcsp.Recv<double>();

        // get ref value
        ref[0] = tcsp.Recv<double>();
        ref[1] = tcsp.Recv<double>();

        // running range set
        if (abs(theta_pitch * 180 / M_PI) > 40)
        {
            voltage[0] = 0.0;
            voltage[1] = 0.0;
        }


        // actuator write
        if (voltage[0] > 15) 
        {
            voltage[0] = 15;
        }
        else if (voltage[0] < -15)
        {
            voltage[0] = -15;
        }
        if (voltage[1] > 15)
        {
            voltage[1] = 15;
        }
        else if (voltage[1] < -15)
        {
            voltage[1] = -15;
        }

        hil_write_analog(board, analog_channels, 2, voltage);

        edc = chrono::high_resolution_clock::now();
        duration = chrono::duration_cast<chrono::nanoseconds>(edc - stc);
        run_time = duration.count() / 1000000;
        stack_time += run_time / 1000;
        cout << " --------------------------------------------------------------------------- " << endl;
        cout << "iter: " << i << " | loop time: " << run_time << "ms | total time: " << stack_time << "s" << endl;
        cout << "motor 1 volt: " << voltage[0] << " | motor 2 volt: " << voltage[1] << endl;
        cout << "pitch: " << theta_pitch * 180 / M_PI << " | yaw: " << theta_yaw * 180 / M_PI << " | pitch_ref: " << ref[0] * 180 / M_PI << " | yaw_ref: " << ref[1] * 180 / M_PI << endl;
    }

    tcsp.Send<string>("end");

    // logic terminate
    voltage[0] = 0.0;
    voltage[1] = 0.0;
    hil_write_analog(board, analog_channels, 2, voltage);
    digital_values[0] = 0;  digital_values[1] = 0;
    hil_write_digital(board, digital_channels, 2, digital_values);
    if (board != NULL)
    {
        hil_close(board);
    }

    return 0;
}
