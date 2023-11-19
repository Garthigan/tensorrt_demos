
import time
import uuid
import paho.mqtt.client as mqtt


def main():

    try:
        mqttBroker = "mqtt.senzmate.com"  # defining the mqtt broker
        file_name1 = "count1.log"
        file_name2 = "count2.log"
        print("script started")

        while True:
            tim = time.localtime()

            if tim.tm_hour < 8:
                print("system in sleep mode")
                break
            file1 = open(file_name1, "r+")
            file2 = open(file_name2, "r+")

            data1 = file1.read()
            data2 = file2.read()

            file1.close()
            file2.close()

            if data1:
                break
            time.sleep(2)
        print("message sending started")


        while True:
            # current time and date local machine
            tim = time.localtime()

            if tim.tm_hour < 8:
                print("system in sleep mode")
                break

            # reset parameters in start of every day.
            if tim.tm_min % 2 == 0 and tim.tm_sec == 2:

                file1 = open(file_name1, "r+")
                file2 = open(file_name2, "r+")
                data1 = file1.read()
                data2 = file2.read()
                file1.close()
                file2.close()

                if not (data1):
                    curr_count1 = "None"
                    count1 = "None"
                else:
                    curr_count1 = int(data1.split()[-2])
                    count1 = int(data1.split()[-1])


                if not (data2):
                    curr_count2 = "None"
                    count2 = "None"
                else:
                    curr_count2 = int(data2.split()[-2])
                    count2 = int(data2.split()[-1])

                if not (data1):
                    continue
                curr_count1 = int(data1.split()[-2])
                count1 = int(data1.split()[-1])

                # add exception to pass mqtt connection issues.
                try:
                    client = mqtt.Client("Nolimit123456")
                    client.connect(mqttBroker)
                    client.publish( topic="D2S/SA/V1/nolimit_mahara_A",
                                    payload="0-CTD:{};1-CT:{};2-CTD:{};3-CT:{};".format(count1,curr_count1,count2,curr_count2),)
                    client.disconnect()
                    time.sleep(100)
                except Exception as ex:
                    print(ex)
                    pass
            else:
                time.sleep(1)

    except Exception as ex:
        exp_file = open("exception.log", "a")
        exp_file.write("{}".format(ex))
        exp_file.close()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except Exception as ex:
        exp_file = open("exception.log", "a")
        exp_file.write("{}".format(ex))
        exp_file.close()