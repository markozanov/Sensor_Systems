from numpy import mean
from matplotlib import pyplot


measurements = [5.2, 9.3, 9.3, 11.0, 6.4, 7.5, 7.4, 6.8, 5.9, 13.1, 11.1, 13.2, 9.6, 8.4, 10.5, 9.4, 6.2, 6.5,
                5.6, 6.6, 7.7, 11.2, 8.1, 9.8, 4.6, 5.7, 10.1, 13.5, 14.1, 12.3, 9.0, 6.7, 6.8, 5.4, 7.6, 10.2,
                11.4, 11.2, 11.5, 7.8, 9.7, 12.4, 13.6, 11.4, 14.0, 10.0, 13.1, 14.2, 12.0, 9.7, 12.4, 12.3, 10.0,
                10.8, 11.9, 14.1, 12.2, 7.3, 8.4, 12.4, 8.7, 13.6, 13.8, 12.4, 8.4, 11.6, 9.6, 12.0, 14.3, 11.4]


measurements_freq_2 = list()
measurements_freq_3 = list()


for i in range (0, len(measurements), 2):
    measurements_freq_2.append(measurements[i])


for i in range (0, len(measurements), 3):
    measurements_freq_3.append(measurements[i])


thresholds = [0.0, 0.2, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0]



def reduced_transmissions(f_measurements, f_thresholds, MA):
    counters_list = list()
    for threshold in f_thresholds:
        counter = 0
        predictions = list()

        for i in range(0, MA):
            predictions.append(f_measurements[i])

        for i in range(MA, len(f_measurements) - MA):
            next_prediction = mean(predictions[-MA:])
            if abs(f_measurements[i] - next_prediction) > threshold:
                counter += 1
                predictions.append(f_measurements[i])
            else:
                predictions.append(next_prediction)

        counters_list.append(counter / len(f_measurements) * 100.0)
    return counters_list


def MSE(f_measurements, f_thresholds, MA):
    errors_list = list()

    for threshold in f_thresholds:
        predictions = list()
        thresh_errors = list()

        for i in range(0, MA):
            predictions.append(f_measurements[i])

        for i in range(MA, len(f_measurements) - MA):
            next_prediction = mean(predictions[-MA:])
            curr_error = f_measurements[i] - next_prediction

            if abs(curr_error) > threshold:
                predictions.append(f_measurements[i])
                thresh_errors.append(curr_error*curr_error)
            else:
                predictions.append(next_prediction)

        errors_list.append(mean(thresh_errors))

    return errors_list


################
# % REDUCED TRANSMISSIONS - FREQUENCY 1
################


# pyplot.subplot(xlabel='Threshold', ylabel='% of reduced transmissions  [Frequency - Every day]',
#                title='Data for NYC daily average high temperatures for 2020')
# pyplot.plot(thresholds, reduced_transmissions(measurements, thresholds, 1),
#             color='red', label='Moving Average - 1', marker='.')
# pyplot.plot(thresholds, reduced_transmissions(measurements, thresholds, 2),
#             color='green', label='Moving Average - 2', marker='.')
# pyplot.plot(thresholds, reduced_transmissions(measurements, thresholds, 3),
#             color='blue', label='Moving Average - 3', marker='.')
# pyplot.legend(loc='best')
# pyplot.show()


################
# % REDUCED TRANSMISSIONS - FREQUENCY 2
################


# pyplot.subplot(xlabel='Threshold', ylabel='% of reduced transmissions  [Frequency - Every 2nd day]',
#                title='Data for NYC daily average high temperatures for 2020')
# pyplot.plot(thresholds, reduced_transmissions(measurements_freq_2, thresholds, 1),
#             color='red', label='Moving Average - 1', marker='.')
# pyplot.plot(thresholds, reduced_transmissions(measurements_freq_2, thresholds, 2),
#             color='green', label='Moving Average - 2', marker='.')
# pyplot.plot(thresholds, reduced_transmissions(measurements_freq_2, thresholds, 3),
#             color='blue', label='Moving Average - 3', marker='.')
# pyplot.legend(loc='best')
# pyplot.show()


################
# % REDUCED TRANSMISSIONS - FREQUENCY 3
################


# pyplot.subplot(xlabel='Threshold', ylabel='% of reduced transmissions  [Frequency - Every 3rd day]',
#                title='Data for NYC daily average high temperatures for 2020')
# pyplot.plot(thresholds, reduced_transmissions(measurements_freq_3, thresholds, 1),
#             color='red', label='Moving Average - 1', marker='.')
# pyplot.plot(thresholds, reduced_transmissions(measurements_freq_3, thresholds, 2),
#             color='green', label='Moving Average - 2', marker='.')
# pyplot.plot(thresholds, reduced_transmissions(measurements_freq_3, thresholds, 3),
#             color='blue', label='Moving Average - 3', marker='.')
# pyplot.legend(loc='best')
# pyplot.show()


#########
# MSE - FREQUENCY 1
#########


# pyplot.subplot(xlabel='Threshold', ylabel='MSE [Frequency - Every day]',
#                title='Data for NYC daily average high temperatures for 2020')
# pyplot.plot(thresholds, MSE(measurements, thresholds, 1),
#             color='red', label='Moving Average - 1', marker='.')
# pyplot.plot(thresholds, MSE(measurements, thresholds, 2),
#             color='green', label='Moving Average - 2', marker='.')
# pyplot.plot(thresholds, MSE(measurements, thresholds, 3),
#             color='blue', label='Moving Average - 3', marker='.')
# pyplot.legend(loc='best')
# pyplot.show()


#########
# MSE - FREQUENCY 2
#########


# pyplot.subplot(xlabel='Threshold', ylabel='MSE [Frequency - Every 2nd day]',
#                title='Data for NYC daily average high temperatures for 2020')
# pyplot.plot(thresholds, MSE(measurements_freq_2, thresholds, 1),
#             color='red', label='Moving Average - 1', marker='.')
# pyplot.plot(thresholds, MSE(measurements_freq_2, thresholds, 2),
#             color='green', label='Moving Average - 2', marker='.')
# pyplot.plot(thresholds, MSE(measurements_freq_2, thresholds, 3),
#             color='blue', label='Moving Average - 3', marker='.')
# pyplot.legend(loc='best')
# pyplot.show()


#########
# MSE - FREQUENCY 3
#########


# pyplot.subplot(xlabel='Threshold', ylabel='MSE [Frequency - Every 3rd day]',
#                title='Data for NYC daily average high temperatures for 2020')
# pyplot.plot(thresholds, MSE(measurements_freq_3, thresholds, 1),
#             color='red', label='Moving Average - 1', marker='.')
# pyplot.plot(thresholds, MSE(measurements_freq_3, thresholds, 2),
#             color='green', label='Moving Average - 2', marker='.')
# pyplot.plot(thresholds, MSE(measurements_freq_3, thresholds, 3),
#             color='blue', label='Moving Average - 3', marker='.')
# pyplot.legend(loc='best')
# pyplot.show()