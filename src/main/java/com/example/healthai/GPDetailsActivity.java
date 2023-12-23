package com.example.healthai;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class GPDetailsActivity extends AppCompatActivity {

    Button homeButton, editGPDetails;
    TextView doctorNameTextView, gpAddressTextView, dateRegisteredTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gp_details);

        homeButton = findViewById(R.id.button_home);
        editGPDetails = findViewById(R.id.button_edit_gp_details);

        doctorNameTextView = findViewById(R.id.textViewDoctorName);
        gpAddressTextView = findViewById(R.id.textViewGPAddress);


        // Retrieve the selected doctor information from the intent
        Intent intent = getIntent();
        if (intent.hasExtra("DOCTOR_INFO")) {
            String selectedDoctorInfo = intent.getStringExtra("DOCTOR_INFO");

            // Split the doctor information into name, address, and other details
            String[] doctorInfoArray = selectedDoctorInfo.split(",");
            String doctorName = doctorInfoArray[0];
            String doctorAddress = doctorInfoArray[1];


            doctorNameTextView.setText(doctorName);
            gpAddressTextView.setText(doctorAddress);

        }

        homeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent homepageActivityIntent = new Intent(GPDetailsActivity.this, HomescreenActivity.class);
                startActivity(homepageActivityIntent);
            }
        });

        editGPDetails.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent editGPDetailsActivityIntent = new Intent(GPDetailsActivity.this, EditGPDetailsActivity.class);
                startActivity(editGPDetailsActivityIntent);
            }
        });
    }
}
