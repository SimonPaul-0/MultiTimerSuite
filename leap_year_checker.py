#include <iostream>
#include <ctime>
#include <vector>
#include <iomanip>
#include <boost/date_time/posix_time/posix_time.hpp>

class Timer {
public:
    Timer() : start_time(0), paused(false) {}

    void start() {
        std::cout << "Timer started." << std::endl;
        start_time = std::time(nullptr);
    }

    void record_lap() {
        if (!paused) {
            double lap_time = std::difftime(std::time(nullptr), start_time);
            lap_times.push_back(lap_time);
            std::cout << "Lap " << lap_times.size() << ": " << format_time(lap_time) << std::endl;
        }
    }

    void pause_resume() {
        if (!paused) {
            std::cout << "Timer paused." << std::endl;
        } else {
            std::cout << "Timer resumed." << std::endl;
        }
        paused = !paused;
    }

    void stop() {
        double total_time = std::difftime(std::time(nullptr), start_time);
        std::cout << "\nTimer stopped." << std::endl;
        std::cout << "Total Elapsed Time: " << format_time(total_time) << std::endl;
        std::cout << "Lap Times:" << std::endl;
        for (std::size_t i = 0; i < lap_times.size(); ++i) {
            std::cout << "Lap " << i + 1 << ": " << format_time(lap_times[i]) << std::endl;
        }
    }

    void show_current_time() {
        time_t now = std::time(nullptr);
        std::cout << "Current Time: " << std::put_time(std::localtime(&now), "%Y-%m-%d %H:%M:%S") << std::endl;
    }

    void show_time_in_country(const std::string& country) {
        boost::posix_time::ptime currentTime = boost::posix_time::second_clock::local_time();
        boost::posix_time::time_duration offset;

        if (country == "New York") {
            offset = boost::posix_time::hours(-5);
        } else if (country == "London") {
            offset = boost::posix_time::hours(0);
        } else if (country == "Tokyo") {
            offset = boost::posix_time::hours(9);
        } else {
            std::cout << "Time zone information not available for " << country << std::endl;
            return;
        }

        boost::posix_time::ptime localTime = currentTime - offset;
        std::cout << "Current Time in " << country << ": "
                  << std::put_time(&localTime, "%Y-%m-%d %H:%M:%S") << std::endl;
    }

private:
    std::time_t start_time;
    std::vector<double> lap_times;
    bool paused;

    static std::string format_time(double seconds) {
        int minutes = static_cast<int>(seconds) / 60;
        seconds = seconds - minutes * 60;
        return std::to_string(minutes) + ":" + std::to_string(seconds);
    }
};

int main() {
    Timer timer;

    try {
        while (true) {
            std::cout << "Enter 'start' to start the timer, 'lap' to record a lap, 'pause' to pause/resume, "
                      << "'stop' to stop the timer, 'time' to show current time, 'zone' to show time in a country, "
                      << "or 'exit' to exit: ";
            std::string user_input;
            std::getline(std::cin, user_input);

            if (user_input == "start") {
                timer.start();
            } else if (user_input == "lap") {
                timer.record_lap();
            } else if (user_input == "pause") {
                timer.pause_resume();
            } else if (user_input == "stop") {
                timer.stop();
            } else if (user_input == "time") {
                timer.show_current_time();
            } else if (user_input == "zone") {
                std::cout << "Enter the country to show time: ";
                std::string country;
                std::getline(std::cin, country);
                timer.show_time_in_country(country);
            } else if (user_input == "exit") {
                break;
            } else {
                std::cout << "Invalid input. Please try again." << std::endl;
            }
        }
    } catch (...) {
        // Handle unexpected exceptions
    }

    return 0;
}
