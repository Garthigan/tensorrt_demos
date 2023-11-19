import time

import paho.mqtt.client as mqtt

import uuid



def main():
    mac_address = uuid.getnode()
    try:
        mqttBroker = "mqtt.senzmate.com"  # defining the mqtt broker
        file_name = "count.log"
    
        print("script started")

        while True:
            tim = time.localtime()

            if tim.tm_hour < 8:
                print("system in sleep mode")
                break
            file = open(file_name, "r+")
            data = file.read()
            file.close()
            if data:
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
                
                file = open(file_name, "r+")
              
                data = file.read()

                file.close()


                if not (data):
                    curr_count = "None"
                    count = "None"
                else:
                    curr_count = int(data.split()[-2])
                    count = int(data.split()[-1])

               
                curr_count = int(data.split()[-2])
                count = int(data.split()[-1])

                # add exception to pass mqtt connection issues.
                try:
                    print(f"{mac_address} ",count,"   ",curr_count)
                    client = mqtt.Client("Nolimit123456")
                    client.connect(mqttBroker)
                    client.publish(
                        topic=f"D2S/SA/V1/{mac_address}/S",
                        payload="0-CTD:{};1-CT:{}".format(
                            count, 
                            curr_count,                                               
                        ),
                    )
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
