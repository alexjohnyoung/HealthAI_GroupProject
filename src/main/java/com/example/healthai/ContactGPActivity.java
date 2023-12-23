package com.example.healthai;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import android.Manifest;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class ContactGPActivity extends AppCompatActivity {

    private static final int REQUEST_CALL_PHONE = 1;
    Button homepageButton;
    Button directionsButton;
    Button bookAppointment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_contact_gp);

        homepageButton = findViewById(R.id.button_homepage);
        directionsButton = findViewById(R.id.button_directions); // Initialize the Directions button

        homepageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Launch the HomescreenActivity
                Intent homescreenActivityIntent = new Intent(ContactGPActivity.this, HomescreenActivity.class);
                startActivity(homescreenActivityIntent);
            }
        });

        Button buttonEmail = findViewById(R.id.button_email_gp);
        buttonEmail.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Launch the email app
                Intent launchEmailAppIntent = new Intent(Intent.ACTION_SENDTO);
                launchEmailAppIntent.setData(Uri.parse("mailto:healthaimobile@gmail.com"));
                startActivity(launchEmailAppIntent);
            }
        });

        bookAppointment = findViewById(R.id.button_book_appointment);
        bookAppointment.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent launchBookAppointemnt = new Intent(ContactGPActivity.this, BookAppointmentActivity.class);
                startActivity(launchBookAppointemnt);
            }
        });

        directionsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Launch the Directions activity
                Intent directionsActivityIntent = new Intent(ContactGPActivity.this, Directions.class);
                startActivity(directionsActivityIntent);
            }
        });

        Button callButton = findViewById(R.id.button_call_gp);

        callButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Check for the CALL_PHONE permission
                if (ContextCompat.checkSelfPermission(ContactGPActivity.this, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
                    // Request the permission
                    ActivityCompat.requestPermissions(ContactGPActivity.this, new String[]{Manifest.permission.CALL_PHONE}, REQUEST_CALL_PHONE);
                } else {
                    // Permission already granted, proceed with the phone call

                    // Replace the phone number with your GP's phone number
                    String phoneNumber = "tel:+353830403490"; // Example phone number

                    // Create an intent with the ACTION_CALL action and the phone number Uri
                    Intent dialIntent = new Intent(Intent.ACTION_CALL, Uri.parse(phoneNumber));

                    // Check if the device can make phone calls (permission and feature)
                    if (dialIntent.resolveActivity(getPackageManager()) != null) {
                        // Start the phone call
                        startActivity(dialIntent);
                    } else {

                    }
                }
            }
        });

    }
}
