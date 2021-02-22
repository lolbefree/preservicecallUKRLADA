import wmi, attribute, sys, os, pyodbc, time


def m1(f1):
    try:
        var = f1
        ip = attribute.ip
        ip = ip + ".stoik.local"
        SW_SHOWNORMAL = 1
        server = ''
        database = ''
        username = ''
        password = ''
        driver = '{SQL Server}'  # Driver you need to connect to the database
        port = '1433'
        cnn = pyodbc.connect(
            'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
            ';PWD=' + password)
        gsalid = var
        cursor = cnn.cursor()

        cursor.execute("select uwtel from gsals01 where gsalid={}".format(gsalid))
        for row in cursor:
            tel = row[0]
            print(tel)

        print("Establishing connection to %s" % ip)
        password = ""
        user_isert = ""

        conn = wmi.WMI(ip, user=r"domain\{}".format(user_isert), password=password)
        process_startup = conn.Win32_ProcessStartup.new()
        process_startup.ShowWindow = SW_SHOWNORMAL
        process_id, result = conn.Win32_Process.Create(
            CommandLine="C:\Program Files\internet explorer\iexplore.exe \"http://localhost:4059/execsvcscript?name=webcall&startparam1={}&startparam2={}\"".format(
                tel, "l"+gsalid), ProcessStartupInformation=process_startup)

        if result == 0:
            print("Process started successfully: %d" % process_id)

        else:
            raise (RuntimeError, "Problem creating process: %d" % result)
            print(tel)
        time.sleep(7)    
        for process in conn.Win32_Process(ProcessId=process_id):
            process.Terminate()
            print(process_id, "killed")
    except Exception as err:
        print(err)
if __name__ == "__main__":
    args = sys.argv[1]
    get_gsalid = m1(args)