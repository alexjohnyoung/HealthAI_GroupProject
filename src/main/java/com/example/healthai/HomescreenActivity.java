package com.example.healthai;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class HomescreenActivity extends AppCompatActivity {

    Button gpDetailsButton, insuranceCompanyButton, paymentMethodButton, medicalRecordsButton, contactGPButton, healthAIButton, reviewsButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_homescreen);
        gpDetailsButton = findViewById(R.id.gp_details);
        insuranceCompanyButton = findViewById(R.id.insurance_company);
        //paymentMethodButton = findViewById(R.id.payment_method);
        //medicalRecordsButton = findViewById(R.id.medical_records);
        contactGPButton = findViewById(R.id.contact_gp);
        healthAIButton = findViewById(R.id.healthAI);
        reviewsButton = findViewById(R.id.reviews);

        gpDetailsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent gpDetailsActivityIntent = new Intent(HomescreenActivity.this, GPDetailsActivity.class);
                startActivity(gpDetailsActivityIntent);
            }
        });

        insuranceCompanyButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent insuranceDetailsActivityIntent = new Intent(HomescreenActivity.this, InsuranceDetailsActivity.class);
                startActivity(insuranceDetailsActivityIntent);
            }
        });

        paymentMethodButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent paymentDetailsActivityIntent = new Intent(HomescreenActivity.this, PaymentDetailsActivity.class);
                startActivity(paymentDetailsActivityIntent);
            }
        });

        medicalRecordsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent medicalRecordsActivityIntent = new Intent(HomescreenActivity.this, MedicalRecordsActivity.class);
                startActivity(medicalRecordsActivityIntent);
            }
        });

        contactGPButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent contactGPActivityIntent = new Intent(HomescreenActivity.this, ContactGPActivity.class);
                startActivity(contactGPActivityIntent);
            }
        });

        healthAIButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent healthAIActivityIntent = new Intent(HomescreenActivity.this, HealthAIActivity.class);
                startActivity(healthAIActivityIntent);
            }
        });

        reviewsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent reviewsActivityIntent = new Intent(HomescreenActivity.this, ReviewActivity.class);
                startActivity(reviewsActivityIntent);
            }
        });




    }

}
