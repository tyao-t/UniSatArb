from masterFunc import *

arbProcess = ArbOpp()

def exit_handler():
    msg = 'Process for: ' + arbProcess.processName + " is terminated"
    perr(msg)
    arbProcess.slackChannel.sendSlack(msg)

def signal_handler(signum, frame):
    # Custom signal handler function to handle specific signals
    # Add additional cleanup tasks or handling for specific signals if needed
    perr(f"Received signal {signum}. Cleaning up before process termination.")
    msg = 'Process for: ' + arbProcess.processName + " is terminated" + "\n" + "signal: "+ str(signum)
    arbProcess.slackChannel.sendSlack(msg)
    exit(1)  # You can choose to exit the process or not depending on your use case

if __name__ == "__main__":  
    arbProcess.slackChannel.startProcessMsg(arbProcess.processName)
    atexit.register(exit_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        while True:
            try:
                now = datetime.now()
                ts = now.strftime("%d/%m/%Y %H:%M:%S")
                btcUSDT = arbProcess.get_usdtFromBTC()
                if btcUSDT is None:
                    continue
                with ThreadPoolExecutor() as executor:
                    # print(btcUSDT)
                    futures = [executor.submit(arbProcess.arbOpp, i, ts, btcUSDT) for i in symbol_Ls]
                    #wait(futures)
                time.sleep(poll_interval)
                
            except Exception as error:
                perr("inner loop")
                perr(error)
                time.sleep(3)
    except KeyboardInterrupt:
        msg = "Process "+ arbProcess.processName + " interrupted by user"
        perr(msg)
        arbProcess.slackChannel.sendSlack(msg)
    except Exception as error:
        arbProcess.slackChannel.killFunction(arbProcess.processName, error)