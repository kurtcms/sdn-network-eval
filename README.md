# Networking: Technical and Commercial Evaluation of a Software-Defined Network (SDN) for a Managed SD-WAN Service

This Python script reads [ping output in Comma Separated Values (CSV) format](https://github.com/kurtcms/pingc) and does the following:

1. Initialise the CSV into classes i.e. objects, by city.
2. Compute and export the hourly and weekly Round Trip Time (RTT) in mean, median, standard deviation, minimum and maximum for a measure of the latency, jitter and packet loss, as well as an overall picture of the data distribution; and the throughput in Megabits per second (Mb/s).
3. Chart the hourly RTT and throughput in four subplots:
  1. The hourly average RTT with its standard deviation plotted as lower and upper band, for a visual illustration of the range of the jitter, bounded by the minimum and maximum, to keep the range within observation;
  2. The hourly average RTT from the regions of evaluation to the respective extended network PoP;
  3. The packet received in percentage (a measure of packet loss) by dividing the hourly Ping data points received, by the hourly Ping data points sent; and
  4. The throughput in Mb/s ranged also by the standard deviation bounded by the observed minimum and maximum, for a visual representation of the network performance during the evaluation period.

Below are the results and charts from an evaluation, comparing the performance between direct internet and an extended network, from December 7th to 14th for Mumbai and Singapore and from December 10th to 17th for Ho Chi Minh City.

A detailed walk-though is available [here](https://kurtcms.org/networking-technical-and-commercial-evaluation-of-a-software-defined-network-sdn-for-a-managed-sd-wan-service/).

## Ho Chi Minh City

With the extended network, jitter from Ho Chi Minh City to Hong Kong dropped by as much as 69% from 5.01ms to 1.66ms while latency increased by 22% from 26.30ms to 32.10ms over direct internet with packet loss holding steady at 0.79%.

![alt text](https://kurtcms.org/git/sdn-network-eval/managed-sd-wan-service-ho-chi-minh-city-hourly-from-2020-12-10-to-2020-12-17.png)

## Mumbai

With the extended network, jitter from Mumbai to Hong Kong dropped by as much as 76% from 5.87ms to 1.42ms while latency increased by 14% from 82.97ms to 94.58ms over direct internet with packet loss holding steady at 0.5%.

![alt text](https://kurtcms.org/git/sdn-network-eval/managed-sd-wan-service-mumbai-hourly-from-2020-12-07-to-2020-12-14.png)

## Singapore

With the extended network, jitter from Singapore to Hong Kong dropped by as much as 53% from 2.53ms to 1.19ms compared to with direct internet while latency and packet loss were holding steady at 35ms and 0.5-0.7% respectively.

![alt text](https://kurtcms.org/git/sdn-network-eval/managed-sd-wan-service-singapore-hourly-from-2020-12-07-to-2020-12-14.png)
