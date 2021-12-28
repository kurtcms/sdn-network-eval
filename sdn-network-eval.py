import sys
import csv
import datetime
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class city:
    '''
    Set the column headers for the ping and iPerf data,
    the date and time for the start and end of the evaluation,
    and a working directory that will be used throughout the class.
    '''
    pcol = ['Date', 'Epoch', 'Dst IP', 'RTT']
    icol = ['Date', 'Src IP', 'Src Port', 'Dst IP', 'Dst Port', 'Int', 'Bytes', 'Bits/s']
    ds = datetime.datetime.strptime('2020-12-07 00:00:00', '%Y-%m-%d %H:%M:%S')
    de = datetime.datetime.strptime('2020-12-14 00:00:00', '%Y-%m-%d %H:%M:%S')
    path = sys.path[0] + '/'

    def __init__(self, p_wg, p_zl, p_hk, i_wg, i_hk):
        '''
        Read the ping and iPerf data given their filenames
        '''
        self.p_wg = pd.read_csv(self.path + p_wg + '.csv',
                                names=self.pcol, header=None, index_col=0,
                                parse_dates=True, squeeze=False)
        self.p_zl = pd.read_csv(self.path + p_zl + '.csv',
                                names=self.pcol, header=None, index_col=0,
                                parse_dates=True, squeeze=False)
        self.p_hk = pd.read_csv(self.path + p_hk + '.csv',
                                names=self.pcol, header=None, index_col=0,
                                parse_dates=True, squeeze=False)
        self.i_wg = pd.read_csv(self.path + i_wg + '.csv',
                                names=self.icol, header=None, index_col=0,
                                parse_dates=True, squeeze=False)
        self.i_hk = pd.read_csv(self.path + i_hk + '.csv',
                                names=self.icol, header=None, index_col=0,
                                parse_dates=True, squeeze=False)

    def __crunch(self, d, d_int, n):
        '''
        Compute and return the mean, median, standard deviation,
        min and max values given the duration and the data type.
        '''
        c = []
        i = 0
        b = 1000000
        while i < n:
            if d_int > 0 and d_int < 8 :
                # Hourly
                ts = (self.ds + datetime.timedelta(hours = i,
                        days = d_int - 1)).strftime('%Y-%m-%d %H:%M:%S')
                te = (self.ds + datetime.timedelta(hours = i + 1,
                        days = d_int - 1)).strftime('%Y-%m-%d %H:%M:%S')
                pktb = 36000
            elif d_int == 0:
                # Daily
                ts = (self.ds + datetime.timedelta(
                        days = i)).strftime('%Y-%m-%d %H:%M:%S')
                te = (self.ds + datetime.timedelta(
                        days = i + 1)).strftime('%Y-%m-%d %H:%M:%S')
                pktb = 864000
            elif d_int == 8:
                # Weekly
                ts = self.ds.strftime('%Y-%m-%d %H:%M:%S')
                te = self.de.strftime('%Y-%m-%d %H:%M:%S')
                pktb = 6048000
            else:
                sys.exit('The date integer provided is out of scope')

            if 'RTT' in d.columns:
                # Ping data
                c.append(
                    {
                        'Date': ts,
                        'RTT Mean': d.loc[ts : te, 'RTT'].mean(),
                        'RTT Median': d.loc[ts : te, 'RTT'].median(),
                        'RTT Std Dev': d.loc[ts : te, 'RTT'].std(),
                        'RTT Min': d.loc[ts : te, 'RTT'].min(),
                        'RTT Max': d.loc[ts : te, 'RTT'].max(),
                        'Pkt Received': d.loc[ts : te, 'RTT'].count()/pktb
                    }
                )
            elif 'Bits/s' in d.columns:
                # iPerf data
                c.append(
                    {
                        'Date': ts,
                        'Bits/s Mean': d.loc[ts : te, 'Bits/s'].mean()/b,
                        'Bits/s Median': d.loc[ts : te, 'Bits/s'].median()/b,
                        'Bits/s Std Dev': d.loc[ts : te, 'Bits/s'].std()/b,
                        'Bits/s Min': d.loc[ts : te, 'Bits/s'].min()/b,
                        'Bits/s Max': d.loc[ts : te, 'Bits/s'].max()/b,
                    }
                )
            else:
                sys.exit('The dataset provided is out of scope')
            i = i + 1
        c = pd.DataFrame(c)
        c.set_index('Date', inplace = True)
        return c

    def daily(self, d):
        '''
        Return the daily RTT and throughput
        '''
        return self.__crunch(d, 0, 6)

    def hourly(self, d):
        '''
        Return the hourly RTT and throughput
        '''
        h = pd.DataFrame([])
        p = 1
        q = 7
        while p < q:
            h = h.append(self.__crunch(d, p, 24))
            p = p + 1
        return h

    def weekly(self, d):
        '''
        Return the weekly RTT and throughput
        '''
        return self.__crunch(d, 8, 1)

    def hourlyd(self, d, d_int):
        '''
        Return the hourly RTT and throughput of a given date
        '''
        if d_int > 0:
            return self.__crunch(d, d_int, 24)
        else:
            sys.exit('The date integer provided is out of scope')

    def ex(self, p1, p2, p3, i1, i2, tl, l1, l2, l3, y1, y2, y3, x3, plot):
        '''
        Export the given RTT and throughput results and
        chart them in four subplots:
        '''
        p1.to_csv(self.path + tl + ' - ' + y1 + ' - ' + l1 + '.csv',
                    index=False, float_format='%.4f')
        p2.to_csv(self.path + tl + ' - ' + y1 + ' - ' + l2 + '.csv',
                    index=False, float_format='%.4f')
        p3.to_csv(self.path + tl + ' - ' + y1 + ' - ' + l3 + '.csv',
                    index=False, float_format='%.4f')
        i1.to_csv(self.path + tl + ' - ' + y3.replace('/', ' per second')
                    + ' - ' + l1 + '.csv',
                    index=False, float_format='%.4f')
        i2.to_csv(self.path + tl + ' - ' + y3.replace('/', ' per second')
                    + ' - ' + l2 + '.csv',
                    index=False, float_format='%.4f')

        if plot == True:
            fig, (mean, zmean, pkt, ipf) = plt.subplots(4, 1,
                                            sharex=True,
                                            figsize=(10, 10))

            # Subplot #1: series #1
            mean.plot(p1.index, p1.loc[:, 'RTT Mean'],
            marker='.', alpha=0.5, linewidth=0.5, label=l1)
            mean.fill_between(p1.index,
            pd.concat([p1.loc[:, 'RTT Mean'] - p1.loc[:, 'RTT Std Dev'],
            p1.loc[:, 'RTT Min']], axis=1).max(axis=1),
            pd.concat([p1.loc[:, 'RTT Mean'] + p1.loc[:, 'RTT Std Dev'],
            p1.loc[:, 'RTT Max']], axis=1).min(axis=1), alpha=0.1)
            # Subplot #2: series #1
            zmean.plot(p3.index, p3.loc[:, 'RTT Mean'], color='green',
            marker='.', alpha=0.5, linewidth=0.5, label=l3)
            # Subplot #3
            pkt.plot(p1.index, p1.loc[:, 'Pkt Received'],
            marker='.', alpha=0.5, linewidth=0.5, label=l1)
            # Subplot #4: series #1
            ipf.plot(i1.index, i1.loc[:, 'Bits/s Mean'],
            marker='.', alpha=0.5, linewidth=0.5, label=l1)
            ipf.fill_between(i1.index,
            pd.concat([i1.loc[:, 'Bits/s Mean'] - i1.loc[:, 'Bits/s Std Dev'],
            i1.loc[:, 'Bits/s Min']], axis=1).max(axis=1),
            pd.concat([i1.loc[:, 'Bits/s Mean'] + i1.loc[:, 'Bits/s Std Dev'],
            i1.loc[:, 'Bits/s Max']], axis=1).min(axis=1), alpha=0.1)

            # Subplot #1: series #2
            mean.plot(p2.index, p2.loc[:, 'RTT Mean'],
            marker='.', alpha=0.5, linewidth=0.5, label=l2)
            mean.fill_between(p2.index,
            pd.concat([p2.loc[:, 'RTT Mean'] - p2.loc[:, 'RTT Std Dev'],
            p2.loc[:, 'RTT Min']], axis=1).max(axis=1),
            pd.concat([p2.loc[:, 'RTT Mean'] + p2.loc[:, 'RTT Std Dev'],
            p2.loc[:, 'RTT Max']], axis=1).min(axis=1), alpha=0.1)
            # Subplot #3: series #2
            pkt.plot(p2.index, p2.loc[:, 'Pkt Received'],
            marker='.', alpha=0.5, linewidth=0.5, label=l2)
            # Subplot #4: series #2
            ipf.plot(i2.index, i2.loc[:, 'Bits/s Mean'],
            marker='.', alpha=0.5, linewidth=0.5, label=l2)
            ipf.fill_between(i2.index,
            pd.concat([i2.loc[:, 'Bits/s Mean'] - i2.loc[:, 'Bits/s Std Dev'],
            i2.loc[:, 'Bits/s Min']], axis=1).max(axis=1),
            pd.concat([i2.loc[:, 'Bits/s Mean'] + i2.loc[:, 'Bits/s Std Dev'],
            i2.loc[:, 'Bits/s Max']], axis=1).min(axis=1), alpha=0.1)

            # Chart options
            fig.suptitle(tl)
            mean.legend()
            mean.set_ylabel(y1)
            zmean.legend()
            zmean.set_ylabel(y1)
            zmean.set_yticks(np.arange(0, 5, 1))
            pkt.legend()
            pkt.set_yticks(np.arange(0.95, 1, 0.01))
            pkt.set_ylabel(y2)
            ipf.legend()
            ipf.set_ylabel(y3)
            ipf.set_xlabel(x3)
            if len(i1.index) > 24:
                ipf.xaxis.set_major_locator(plt.MaxNLocator(24))
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig(tl + '.png')
            #plt.show()

if __name__ == '__main__':
    '''
    Create the city objects given their respective ping and iPerf
    data, compute and export the hourly and weekly RTT and throughput,
    and chart the hourly RTT and throughput.
    '''
    mb = city('ping-mb-10.1.1.1',
                'ping-mb-45.43.45.141',
                'ping-mb-18.163.161.217',
                'iperf-mb-10.1.1.1',
                'iperf-mb-18.163.161.217')

    sg = city('ping-sg-10.1.1.1',
                'ping-sg-129.227.67.94',
                'ping-sg-18.163.161.217',
                'iperf-sg-10.1.1.1',
                'iperf-sg-18.163.161.217')

    hc = city('ping-hc-10.1.1.1',
                'ping-hc-122.10.140.2',
                'ping-hc-18.163.161.217',
                'iperf-hc-10.1.1.1',
                'iperf-hc-18.163.161.217')
    '''
    Adjust the date and time for the start and end of
    the evaluation for Ho Chi Minh City
    '''
    hc.ds = datetime.datetime.strptime('2020-12-10 00:00:00', '%Y-%m-%d %H:%M:%S')

    mb.ex(mb.hourly(mb.p_wg),
            mb.hourly(mb.p_hk),
            mb.hourly(mb.p_zl),
            mb.hourly(mb.i_wg),
            mb.hourly(mb.i_hk),
            'Mumbai (Hourly from 2020-12-07 to 2020-12-14)',
            'Extended Network Service',
            'Internet',
            'AWS Mumbai to Extended Network Mumbai PoP',
            'RTT (ms)',
            'Pkt Received (%)',
            'Throughput (Mbits/s)',
            'Date and Time',
            True)

    sg.ex(sg.hourly(sg.p_wg),
            sg.hourly(sg.p_hk),
            sg.hourly(sg.p_zl),
            sg.hourly(sg.i_wg),
            sg.hourly(sg.i_hk),
            'Singapore (Hourly from 2020-12-07 to 2020-12-14)',
            'Extended Network Service',
            'Internet',
            'AWS Singapore to Extended Network Singapore PoP',
            'RTT (ms)',
            'Pkt Received (%)',
            'Throughput (Mbits/s)',
            'Date and Time',
            True)

    hc.ex(hc.hourly(hc.p_wg),
            hc.hourly(hc.p_hk),
            hc.hourly(hc.p_zl),
            hc.hourly(hc.i_wg),
            hc.hourly(hc.i_hk),
            'Ho Chi Minh City (Hourly from 2020-12-10 to 2020-12-17)',
            'Extended Network Service',
            'Internet',
            'VinaHost.vn Ho Chi Minh City to Extended Network Ho Chi Minh City PoP',
            'RTT (ms)',
            'Pkt Received (%)',
            'Throughput (Mbits/s)',
            'Date and Time',
            True)

    mb.ex(mb.weekly(mb.p_wg),
            mb.weekly(mb.p_hk),
            mb.weekly(mb.p_zl),
            mb.weekly(mb.i_wg),
            mb.weekly(mb.i_hk),
            'Mumbai (From 2020-12-07 to 2020-12-14)',
            'Extended Network Service',
            'Internet',
            'AWS Mumbai to Extended Network Mumbai PoP',
            'RTT (ms)',
            'Pkt Received (%)',
            'Throughput (Mbits/s)',
            'Date and Time',
            False)

    sg.ex(sg.weekly(sg.p_wg),
            sg.weekly(sg.p_hk),
            sg.weekly(sg.p_zl),
            sg.weekly(sg.i_wg),
            sg.weekly(sg.i_hk),
            'Singapore (Hourly from 2020-12-10 to 2020-12-17)',
            'Extended Network Service',
            'Internet',
            'AWS Singapore to Extended Network Singapore PoP',
            'RTT (ms)',
            'Pkt Received (%)',
            'Throughput (Mbits/s)',
            'Date and Time',
            False)

    hc.ex(hc.weekly(hc.p_wg),
            hc.weekly(hc.p_hk),
            hc.weekly(hc.p_zl),
            hc.weekly(hc.i_wg),
            hc.weekly(hc.i_hk),
            'Ho Chi Minh City (From 2020-12-07 to 2020-12-14)',
            'Extended Network Service',
            'Internet',
            'VinaHost.vn Ho Chi Minh City to Extended Network Ho Chi Minh City PoP',
            'RTT (ms)',
            'Pkt Received (%)',
            'Throughput (Mbits/s)',
            'Date and Time',
            False)
