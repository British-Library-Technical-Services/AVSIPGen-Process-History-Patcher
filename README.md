# Process History Patcher README

A simple GUI application to copy Process History metadata between Submision Information Packages (SIP) in the British Library's [AV SIP Generator](https://british-library-technical-services.github.io/Documentation/docs/AVSIPGEN/)

The application utlises the AV SIP Generator API to capture Process History metadata in JSON format from a Reference SIP and copies it to a Destination SIP.  The Reference and Destination SIPs are defined by their [SIP Id]()
<!---insert link--->

## Use

![GUI_IMG](https://user-images.githubusercontent.com/66015813/225941699-0a76bfe6-7c3e-430e-8c93-82b0c5f22aad.PNG)

1. Enter the Id for the **Reference SIP** you would like to capture the Process History from
2. Enter the Id for the **Destination SIP** you would like to copy the Process History to
3. Press the **<< PATCH >>** button

The SIP Id will be checked to confirm it is a valid.  The Process History will then be captured and copied to the Destination SIP.  A SUCCESS status will be returned in the bottom status bar once complete.  

Referesh the Process History page in the browser and the Process History will be populated with the data from the Reference SIP.




