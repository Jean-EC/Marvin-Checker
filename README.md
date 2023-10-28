# Marvin-Checker

This script is designed to be run in a cronjob every 5 minutes. It checks if Marvin is available and sends a notification if he is not.

## Usage

To use this script, you need to add it to your crontab. Here's an example of how to do it:

1. Open your crontab file by running `crontab -e` in your terminal.
2. Add the following line to the file: `*/5 * * * * python3 /path/to/marvinCheck.py > /dev/null 2>&1`
3. Replace `/path/to/marvin-checker.sh` with the actual path to the script on your system.

Make sure to change the `options.profile` variable in the script to your own profile.

Feel free to fork it to adapt it for an other browser.
## License

This script is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.


