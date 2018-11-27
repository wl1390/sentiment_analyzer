package com.twitteranalyzer.twitteanalyzer;

import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;


import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.google.gson.JsonObject;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
        getSupportActionBar().hide();

        final Button button = findViewById(R.id.b_start);
        final EditText userinput = findViewById(R.id.user_input);



        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                try {
                    String temp = userinput.getText().toString();
                    userinput.setText("");
                    display(Analyzer.analyze(temp));

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });

    }

    protected void display(String message) throws JSONException {
        TextView result = findViewById(R.id.result);
        result.setText("waiting...");
        JSONObject reader = new JSONObject(message);
        JSONArray document = reader.getJSONArray("documents");


        String score = String.valueOf(document.getJSONObject(0).getDouble("score"));

        result.setText(score);
    }

}
