using UnityEngine;
using System.IO.Ports;

public class ReadUSB : MonoBehaviour {

    const int baudrate = 115200;

    const string portName = "/dev/cu.usbmodem2815121";

    SerialPort serialPort = new SerialPort(portName, baudrate);



    void Start () {
            serialPort.ReadTimeout = 100;
            serialPort.Open();

            if( !serialPort.IsOpen ) {

                    Debug.LogError("Couldn't open " + portName);

            }
    }


    void Update () {

            string buffer = serialPort.ReadExisting();

            string[] lines = buffer.Split( '\n' );

            if ( lines.Length >= 2) {

                    string[] line = lines[lines.Length - 2].Split( ' ' );

                    if ( line[0] == "QC" ) {

                            Quaternion q = new Quaternion( float.Parse(line[2]),
                                                           float.Parse(line[3]),
                                                          -float.Parse(line[4]),
                                                           float.Parse(line[1]));

                            transform.rotation = Quaternion.Inverse(q);

                    }

            }

    }


    void OnGUI()
    {
            string euler = "Euler angle: " + transform.eulerAngles.x + ", " +
                           transform.eulerAngles.y + ", " + transform.eulerAngles.z;

            GUI.Label(new Rect(10,10,500,100), euler);
    }
}
