package com.example.remotesocket2;

import android.graphics.Color;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.textfield.TextInputEditText;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Calendar;
import java.util.Objects;

public class MainActivity extends AppCompatActivity {

    // fields in homepage
    public ToggleButton connectionStatus, syncButton, switchButton, pumpA, pumpB, pumpC, pumpD;
    public TextView messageLog, csvLog;
    public TextInputEditText messageBox;
    public static String message;
    public ImageButton saveButton, timeButton, tempButton, gpsButton, clearButton, sendButton;

    // file for .csv file to be written to android/data/...
    public static String fileName = "";

    // server info
    ServerSocket serverSocket;
    public static String SERVER_IP = "";
    public final int SERVER_PORT = 10000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Hide title bar
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        Objects.requireNonNull(getSupportActionBar()).hide();

        // Prevent device from sleeping
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        setContentView(R.layout.activity_main);

        connectionStatus = findViewById(R.id.tvIP);
        messageLog = findViewById(R.id.body1);
        csvLog = findViewById(R.id.body2);
        messageBox = findViewById(R.id.inputText1);

        syncButton = findViewById(R.id.button2);
        saveButton = findViewById(R.id.button3);
        timeButton = findViewById(R.id.button4);
        tempButton = findViewById(R.id.button5);
        gpsButton = findViewById(R.id.button6);
        clearButton = findViewById(R.id.button7);
        sendButton = findViewById(R.id.button8);

        switchButton = findViewById(R.id.buttonPumpSwitch);
        pumpA = findViewById(R.id.buttonPumpA);
        pumpB = findViewById(R.id.buttonPumpB);
        pumpC = findViewById(R.id.buttonPumpC);
        pumpD = findViewById(R.id.buttonPumpD);

        // Assigns local ip address to SERVER_IP
        try {
            SERVER_IP = getIP();
        } catch (UnknownHostException e){
            e.printStackTrace();
        }

        // Starts Thread 1
        new Thread(new Thread1()).start();
    }

    // Gets local ip address
    private String getIP() throws UnknownHostException {
        WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        assert wifiManager != null;
        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        int INT_IP = wifiInfo.getIpAddress();
        return InetAddress.getByAddress(ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putInt(INT_IP).array()).getHostAddress();
    }

    // Writes to csv file
    private void csvWriter() {
        fileName = getDateTime("millis") + ".csv";
        File externalFile = new File (getExternalFilesDir(""), fileName);
        try {
            FileOutputStream fos = new FileOutputStream(externalFile);
            fos.write(csvLog.getText().toString().getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
        Toast.makeText(getApplicationContext(), "File saved to:\n/Android/data/com.example.remotesocket2/files", Toast.LENGTH_LONG).show();
    }

    // Gets date and time
    private String getDateTime(String s) {
        String year = String.valueOf(Calendar.getInstance().get(Calendar.YEAR));
        String month = String.valueOf(Calendar.getInstance().get(Calendar.MONTH));
        String day = String.valueOf(Calendar.getInstance().get(Calendar.DATE));
        String hour = String.valueOf(Calendar.getInstance().get(Calendar.HOUR_OF_DAY));
        String minute = String.valueOf(Calendar.getInstance().get(Calendar.MINUTE));
        String second = String.valueOf(Calendar.getInstance().get(Calendar.SECOND));
        String millis = String.valueOf(Calendar.getInstance().getTimeInMillis());

        if (month.length() == 1)
            month = "0" + month;
        if (day.length() == 1)
            day = "0" + day;
        if (hour.length() == 1)
            hour = "0" + hour;
        if (minute.length() == 1)
            minute = "0" + minute;
        if (second.length() == 1)
            second = "0" + second;

        String date = year + "-" + month + "-" + day;
        String time = hour + ":" + minute + ":" + second;

        switch (s) {
            case "date":
                return date;
            case "time":
                return time;
            case "millis":
                return millis;
        }
        return "date" + " " + "time";
    }

    // Function for pump clicks
    public void pumpClick (View view) {
        int viewID = view.getId();
        message = " ";

        // PUMP A
        if (viewID == R.id.buttonPumpA) {
            message = "pumpStopA";
            if (pumpA.isChecked())
                message = "pumpA";
            pumpD.setEnabled(!pumpA.isChecked());
        }

        // PUMP B
        if (viewID == R.id.buttonPumpB) {
            message = "pumpStopB";
            if (pumpB.isChecked())
                message = "pumpB";
            pumpC.setEnabled(!pumpB.isChecked());
        }

        // PUMP C
        if (viewID == R.id.buttonPumpC) {
            message = "pumpStopC";
            if (pumpC.isChecked())
                message = "pumpC";
            pumpB.setEnabled(!pumpC.isChecked());
        }

        // PUMP D
        if (viewID == R.id.buttonPumpD) {
            message = "pumpStopD";
            if (pumpD.isChecked())
                message = "pumpD";
            pumpA.setEnabled(!pumpD.isChecked());
        }

        // COLD SEEK SWITCH
        else if (viewID == R.id.buttonPumpSwitch) {
            message = "switch";

            pumpA.setEnabled(!switchButton.isChecked());
            pumpB.setEnabled(!switchButton.isChecked());
            pumpC.setEnabled(!switchButton.isChecked());
            pumpD.setEnabled(!switchButton.isChecked());
        }

        // SEND
        new Thread(new Thread4(message)).start();
    }

    // Functions for button clicks
    public void buttonClick (View view) {
        int viewID = view.getId();
        message = " ";

        // EXIT
        if (viewID == R.id.button1)
            finish();

        // EXPORT FILE
        else if (viewID == R.id.button3)
            csvWriter();

        // TIME
        else if (viewID == R.id.button4)
            messageLog.append("\nServer: Time\nServer: " + getDateTime("time"));

        // CLEAR
        else if (viewID == R.id.button7) {
            messageLog.setText(R.string.message_log);
            csvLog.setText(R.string.csvHead);
        }

        else {
            // SYNC
            if (viewID == R.id.button2) {
                saveButton.setEnabled(!syncButton.isChecked());
                timeButton.setEnabled(!syncButton.isChecked());
                tempButton.setEnabled(!syncButton.isChecked());
                gpsButton.setEnabled(!syncButton.isChecked());
                clearButton.setEnabled(!syncButton.isChecked());
                sendButton.setEnabled(!syncButton.isChecked());
                message = "update";
            }

            // TEMPERATURE
            else if (viewID == R.id.button5)
                message = "temp";

            // GPS
            else if (viewID == R.id.button6)
                message = "gps";

            // SEND
            else
                message = Objects.requireNonNull(messageBox.getText()).toString();

            messageBox.setText("");
            new Thread(new Thread3(message)).start();
        }
    }

    // Thread 1 variables
    private PrintWriter output;
    private BufferedReader input;

    // Thread 1 code - establishes connection with client
    class Thread1 implements Runnable {
        @Override
        public void run() {
            Socket socket;
            try {
                serverSocket = new ServerSocket(SERVER_PORT);
                runOnUiThread(() -> connectionStatus.setText(SERVER_IP));
                try {
                    socket = serverSocket.accept();
                    output = new PrintWriter(socket.getOutputStream());
                    input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    runOnUiThread(() -> {
                        connectionStatus.setChecked(true);
                        connectionStatus.setTextColor(Color.GREEN);
                    });
                    new Thread(new Thread2()).start();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // Thread 2 code - fetches message from client to server
    private class Thread2 implements Runnable {
        @Override
        public void run() {
            while (true) {
                try {
                    final String message = input.readLine();
                    if (message != null) {
                        if (syncButton.isChecked()) {
                            runOnUiThread(() -> csvLog.append("\""+ message + "\","));
                        }
                        else {
                            runOnUiThread(() -> messageLog.append(message));
                        }
                    }
                    else {
                        new Thread(new Thread1()).start();
                        return;
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    // Thread 3 code - writes message from server to client
    private class Thread3 implements Runnable {
        private final String message;
        Thread3(String message) {
            this.message = message;
        }

        @Override
        public void run() {
            do {
                // no loop
                if (!message.equals("update")) {
                    messageLog.append("\nServer: " + message + "\nClient: ");
                    output.write(message);
                    output.flush();
                }
                // loop until sync untoggled
                else {
                    output.write("update");
                    output.flush();
                    try {
                        runOnUiThread(() -> csvLog.append("\n\"" + getDateTime("time") + "\","));
                        Thread.sleep(10000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            } while (syncButton.isChecked());
        }
    }

    // Thread 4 code - controls pumps
    private class Thread4 implements Runnable {
        private final String message;
        Thread4(String message) {
            this.message = message;
        }

        @Override
        public void run() {
            String[] pumps = {"pumpAB", "pumpAC", "pumpBD", "pumpCD"};
            // random motor
            if (message.equals("pumpSwitch")) output.write(pumps[(int) Math.floor(Math.random() * 4)]);
            // individual motor
            else output.write(message);
            output.flush();
        }
    }
}