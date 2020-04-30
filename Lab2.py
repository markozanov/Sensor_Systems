from numpy import mean
import numpy as NP
from matplotlib import pyplot


measurements_temp = [5.2, 9.3, 9.3, 11.0, 6.4, 7.5, 7.4, 6.8, 5.9, 13.1, 11.1, 13.2, 9.6, 8.4, 10.5, 9.4, 6.2, 6.5,
                5.6, 6.6, 7.7, 11.2, 8.1, 9.8, 4.6, 5.7, 10.1, 13.5, 14.1, 12.3, 9.0, 6.7, 6.8, 5.4, 7.6, 10.2,
                11.4, 11.2, 11.5, 7.8, 9.7, 12.4, 13.6, 11.4, 14.0, 10.0, 13.1, 14.2, 12.0, 9.7, 12.4, 12.3, 10.0,
                10.8, 11.9, 14.1, 12.2, 7.3, 8.4, 12.4, 8.7, 13.6, 13.8, 12.4, 8.4, 11.6, 9.6, 12.0, 14.3, 11.4]


measurements_humid = [60, 55, 45, 47, 53, 81, 82, 80, 75, 71, 68, 68, 64, 53, 50, 52, 63, 78, 88, 80, 70, 75, 60, 60,
                      60, 83, 80, 75, 55, 50, 49, 52, 66, 65, 69, 73, 77, 61, 62, 63, 60, 68, 70, 51, 45, 40, 48, 71,
                      60, 62, 75, 77, 83, 63, 60, 58, 58, 55, 49, 61, 62, 63, 64, 77, 50, 52, 66, 70, 80, 48]

measurements_temp_freq_2 = list()
measurements_temp_freq_3 = list()


measurements_humid_freq_2 = list()
measurements_humid_freq_3 = list()


for i in range(0, len(measurements_temp), 2):
    measurements_temp_freq_2.append(measurements_temp[i])
    measurements_humid_freq_2.append(measurements_humid[i])


for i in range(0, len(measurements_temp), 3):
    measurements_temp_freq_3.append(measurements_temp[i])
    measurements_humid_freq_3.append(measurements_humid[i])


thresholds_temp = [0.0, 0.2, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0]
thresholds_humid = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]


def reduced_transmissions(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA):
    counters_list = {}
    for threshold in f_thresholds_temp:
        for threshold_h in f_thresholds_humid:
            counter = 0
            predictions_temp = list()
            predictions_humid = list()

            for i in range(0, MA):
                predictions_temp.append(f_measurements_temp[i])
                predictions_humid.append(f_measurements_humid[i])

            for i in range(MA, len(f_measurements_temp) - MA):
                next_prediction_temp = mean(predictions_temp[-MA:])
                next_prediction_humid = mean(predictions_humid[-MA:])
                if (abs(f_measurements_temp[i] - next_prediction_temp) > threshold) \
                        and\
                        (abs(f_measurements_humid[i] - next_prediction_humid) > threshold_h):
                    counter += 1
                    predictions_temp.append(f_measurements_temp[i])
                    predictions_humid.append(f_measurements_humid[i])
                else:
                    predictions_temp.append(next_prediction_temp)
                    predictions_humid.append(next_prediction_humid)

            counters_list.update({str(threshold) + ';' + str(threshold_h): counter / len(f_measurements_temp) * 100.0})
    return counters_list


def MSE(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA):
    errors_list = {}

    for threshold in f_thresholds_temp:
        for threshold_h in f_thresholds_humid:
            predictions_temp = list()
            predictions_humid = list()
            thresh_errors = list()

            for i in range(0, MA):
                predictions_temp.append(f_measurements_temp[i])
                predictions_humid.append(f_measurements_humid[i])

            for i in range(MA, len(f_measurements_temp) - MA):
                next_prediction_temp = mean(predictions_temp[-MA:])
                next_prediction_humid = mean(predictions_humid[-MA:])
                curr_error_temp = f_measurements_temp[i] - next_prediction_temp
                curr_error_humid = f_measurements_humid[i] - next_prediction_humid

                if abs(curr_error_temp) > threshold and abs(curr_error_humid) > threshold_h:
                    predictions_temp.append(f_measurements_temp[i])
                    predictions_humid.append(f_measurements_humid[i])
                    thresh_errors.append(pow(curr_error_humid, 2) + pow(curr_error_temp, 2))
                else:
                    predictions_temp.append(next_prediction_temp)

            errors_list.update({str(threshold) + ';' + str(threshold_h): mean(thresh_errors)})

    return errors_list


def plotting_function_rt(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA, F):
    result = reduced_transmissions(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA)
    x = NP.array(list(map(lambda k: float(k.split(';')[0]), result.keys())))
    y = NP.array(list(map(lambda k: float(k.split(';')[1]), result.keys())))
    val = NP.array(list(result.values()))

    pyplot.xticks(NP.arange(NP.amin(x), NP.ceil(NP.amax(x)) + 1))
    pyplot.yticks(NP.arange(NP.amin(y), NP.ceil(NP.amax(y)) + 1))
    pyplot.scatter(x, y, c=val, s=100)
    pyplot.title(f'% reduced transmissions - Moving Average ' + str(MA) + ' Frequency Every ' + str(F) + ' day')
    pyplot.xlabel('Temperature thresholds')
    pyplot.ylabel('Humidity thresholds')
    pyplot.colorbar()
    pyplot.show()


def plotting_function_mse(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA, F):
    result = MSE(f_measurements_temp, f_measurements_humid, f_thresholds_temp, f_thresholds_humid, MA)
    x = NP.array(list(map(lambda k: float(k.split(';')[0]), result.keys())))
    y = NP.array(list(map(lambda k: float(k.split(';')[1]), result.keys())))
    val = NP.array(list(result.values()))

    pyplot.xticks(NP.arange(NP.amin(x), NP.ceil(NP.amax(x)) + 1))
    pyplot.yticks(NP.arange(NP.amin(y), NP.ceil(NP.amax(y)) + 1))
    pyplot.scatter(x, y, c=val, s=100)
    pyplot.title(f'MSE - Moving Average ' + str(MA) + ' Frequency Every ' + str(F) + ' day')
    pyplot.xlabel('Temperature thresholds')
    pyplot.ylabel('Humidity thresholds')
    pyplot.colorbar()
    pyplot.show()


################
# % REDUCED TRANSMISSIONS - FREQUENCY 1
################

plotting_function_rt(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 1, 1)
plotting_function_rt(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 2, 1)
plotting_function_rt(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 3, 1)

################
# % REDUCED TRANSMISSIONS - FREQUENCY 2
################

plotting_function_rt(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 1, 2)
plotting_function_rt(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 2, 2)
plotting_function_rt(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 3, 2)


################
# % REDUCED TRANSMISSIONS - FREQUENCY 3
################

plotting_function_rt(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 1, 3)
plotting_function_rt(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 2, 3)
plotting_function_rt(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 3, 3)

#########
# MSE - FREQUENCY 1
#########

plotting_function_mse(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 1, 1)
plotting_function_mse(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 2, 1)
plotting_function_mse(measurements_temp, measurements_humid, thresholds_temp, thresholds_humid, 3, 1)

#########
# MSE - FREQUENCY 2
#########

plotting_function_mse(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 1, 2)
plotting_function_mse(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 2, 2)
plotting_function_mse(measurements_temp_freq_2, measurements_humid_freq_2, thresholds_temp, thresholds_humid, 3, 2)

#########
# MSE - FREQUENCY 3
#########

plotting_function_mse(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 1, 3)
plotting_function_mse(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 2, 3)
plotting_function_mse(measurements_temp_freq_3, measurements_humid_freq_3, thresholds_temp, thresholds_humid, 3, 3)
