package com.example.artbaryl.firehelper;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void Help(View view) {
        Intent Help = new Intent(this, MapsActivityCurrentPlace.class);
        startActivity(Help);
    }

    public void noHelp(View view) {
    }
}
