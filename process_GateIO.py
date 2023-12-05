from masterFunc import *

gateioInstance = GateIO()

def exit_handler():
    msg = 'Process for: ' + gateioInstance.processName + " is terminated"
    perr(msg)
    gateioInstance.slackChannel.sendSlack(msg)
def signal_handler(signum, frame):
    # Custom signal handler function to handle specific signals
    # Add additional cleanup tasks or handling for specific signals if needed
    perr(f"Received signal {signum}. Cleaning up before process termination.")
    msg = 'Process for: ' + gateioInstance.processName + " is terminated" + "\n" + "signal: "+ str(signum)
    gateioInstance.slackChannel.sendSlack(msg)
    exit(1)  # You can choose to exit the process or not depending on your use case

if __name__ == "__main__":  
    gateioInstance.slackChannel.startProcessMsg(gateioInstance.processName)
    atexit.register(exit_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    print("here")
    try:
        while True:
            try:
                with ThreadPoolExecutor() as executor:
                    futures = [executor.submit(gateioInstance.gateIO_redis, i) for i in symbol_Ls]
                    #wait(futures)
                time.sleep(poll_interval)

            except Exception as error:
                perr("inner loop ")
                perr(error)
                time.sleep(3)
    except KeyboardInterrupt:
        msg = "Process "+ gateioInstance.processName + " interrupted by user"
        perr(msg)
        gateioInstance.slackChannel.sendSlack(msg)
    except Exception as error:
        gateioInstance.slackChannel.killFunction(gateioInstance.processName, error)