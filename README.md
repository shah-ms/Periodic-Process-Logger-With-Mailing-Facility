# Periodic-Process-Logger-With-Mailing-Facility
This project helps in automating process log activity using Python libraries. A log file is created periodically, using scheduler of Python, containing process related information like name, pid, thread count, memory usage, etc &amp; then that log file will be sent to specified email address.

To run this automation script, it needs 3 command-line arguments.

1st - the Directory Name which will be created (if does not exists) which will contain the log files

2nd - email id of the receiver

3rd - number of minutes after which you want the log file to be created and sent via mail
