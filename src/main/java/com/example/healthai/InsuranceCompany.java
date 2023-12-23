package com.example.healthai;

import java.util.Date;

public class InsuranceCompany {

    String companyName;
    String policyNumber;
    String mobileNumber;
    Boolean coverage;

    InsuranceCompany(String companyName, String policyNumber, String mobileNumber, Boolean coverage){
        this.companyName = companyName;
        this.policyNumber = policyNumber;
        this.mobileNumber = mobileNumber;
        this.coverage = coverage;
    }

    public String getCompanyName() {
        return companyName;
    }

    public void setCompanyName(String companyNme) {
        this.companyName = companyName;
    }
    public String getPolicyNumber() {
        return policyNumber;
    }

    public void setPolicyNumber(String policyNumber) {
        this.policyNumber = policyNumber;
    }

    public String getMobileNumber() {
        return mobileNumber;
    }

    public void setMobileNumber(String mobileNumber) {
        this.mobileNumber = mobileNumber;
    }

    public boolean coverage() {
        return coverage;
    }

    public void setCoverage(boolean coverage) {
        this.coverage = coverage;
    }

}
