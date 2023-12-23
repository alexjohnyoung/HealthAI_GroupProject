package com.example.healthai;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

public class InsuranceDetailsActivity extends AppCompatActivity {

    Button editInsuranceButton, homepageButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_insurance_details);
        editInsuranceButton = findViewById(R.id.button_edit_insurance);
        homepageButton = findViewById(R.id.button_home_page);

        editInsuranceButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent editInsuranceDetailsActivityIntent = new Intent(InsuranceDetailsActivity.this, EditInsuranceActivity.class);
                startActivity(editInsuranceDetailsActivityIntent);
            }
        });

        homepageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent HomescreenActivityIntent = new Intent(InsuranceDetailsActivity.this, HomescreenActivity.class);
                startActivity(HomescreenActivityIntent);
            }
        });

    }
}
