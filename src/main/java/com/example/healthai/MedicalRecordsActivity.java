package com.example.healthai;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class MedicalRecordsActivity extends AppCompatActivity {

    Button homepageButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activtiy_medical_records);
        homepageButton = findViewById(R.id.button_homepage);

        homepageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent HomescreenActivityIntent = new Intent(MedicalRecordsActivity.this, HomescreenActivity.class);
                startActivity(HomescreenActivityIntent);
            }
        });

    }

}
