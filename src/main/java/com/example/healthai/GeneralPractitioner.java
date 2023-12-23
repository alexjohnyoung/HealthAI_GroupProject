package com.example.healthai;

import java.util.Date;

public class GeneralPractitioner {

    String name, address;
    Date dateRegistered;

    Boolean medicalCard;

    GeneralPractitioner(String name, String address, Date dateRegistered, Boolean medicalCard){
        this.name = name;
        this.address = address;
        this.dateRegistered = dateRegistered;
        this.medicalCard = medicalCard;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public Date getDateRegistered() {
        return dateRegistered;
    }

    public void setDate(Date dateRegistered) {
        this.dateRegistered = dateRegistered;
    }

    public boolean medicalCard() {
        return medicalCard;
    }

    public void setMedicalCard(boolean medicalCard) {
        this.medicalCard = medicalCard;
    }
}
