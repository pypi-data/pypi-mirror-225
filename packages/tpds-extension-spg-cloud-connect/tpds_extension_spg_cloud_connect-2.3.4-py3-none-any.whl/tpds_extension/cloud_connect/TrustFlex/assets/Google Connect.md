# Trust Platform Design Suite - Usecase Help - Google Connect

This document helps to understand Pre and Post steps of Usecase transaction diagram.

## Setup requirements
 - [DM320118](https://www.microchip.com/developmenttools/ProductDetails/DM320118)
 - [WIFI 7 CLICK](https://www.mikroe.com/wifi-7-click)
 - [MPLAB X IDE](https://www.microchip.com/en-us/development-tools-tools-and-software/mplab-x-ide) 5.45 or above

## Pre Usecase transaction Steps
 - Connect DM320118 board to PC running Trust Platform Design Suite
 - Ensure *MPLAB X Path* is set in *File* -> *Preference* under *System Settings*. This helps
    - To program the Usecase prototyping kit to factory reset application by TPDS
    - To open the embedded project of the Usecase
 - Setup GCP account. Follow the instructions at [**GCP demo account setup**](#gcp-account-setup-instructions)
 - Ensure *~/.trustplatform/gcp_credentials.yaml* contains the account credentials.
    - ~ indicates home directory.
        - Windows home directory is \user\username
        - Mac home directory is /users/username
        - Most Linux/Unix home directory is /home/username
 - Note that *~/.trustplatform/spg_cloud_connect* is the **Usecase working directory**. It contains the resources generated during transaction diagram execution.
 - On older versions of WIFI 7 click boards, It is required to upgrade the WIFI 7 click board firmware.
    - Run the *winc_firmware_update.bat* batch file in *~/.trustplatform/winc_firmware_upgrade*.
        - Note1: This requires [Microchip/Atmel Studio](https://www.microchip.com/en-us/development-tools-tools-and-software/microchip-studio-for-avr-and-sam-devices) installed on the system. It works only on Windows.
        - Note2: Some versions of DM320118 nEDBG firmware fails to upgrade winc software. In such cases, upgrade the firmware to 1.18.528 as below and try running above batch file.
            - Open Microchip Studio Command Prompt, navigate to *~/.trustplatform/winc_firmware_upgrade* folder and run the below command.
                - *atfw -t nedbg -a nedbg_fw-1.18.528.zip*
        - Note3: Winc firmware upgrade process can take a while, wait for it to complete.

## Post Usecase transaction Steps
On completing Usecase steps execution on TPDS, it is possible to either run the embedded project or view C source files by clicking *MPLAB X Project* or *C Source Folder* button.

- Once the Usecase project is loaded on MPLAB X IDE,
    - Set the project as Main -> right click on Project and select *Set as Main Project*
    - Set WiFi SSID and Password -> Open *cloud_wifi_config.h* under Project Header Files -> common -> cloud_wifi_config.h.
        - Uncomment and update WLAN_SSID and WLAN_PSK macros with user's wifi SSID and password
    - Set the configuration -> right click on Project, expand *Set Configuration* to select *GOOGLE_CONNECT*
    - Build and Program the project -> right click on Project and select *Make and Program Device*
- Log from the embedded project can be viewed using applications like TeraTerm. Select the COM port and set baud rate as 115200-8-N-1

Example TeraTerm log after successfully executing embedded project:

- Connecting to Cloud messages appear along with the led state.

![GCP Connect TeraTerm Log](images/gcp_ttlog.png "GCP Connect TeraTerm Log")


## GCP Account Setup Instructions
This document mainly focuses on how-to setup the google cloud account For connecting the trust platform devices to cloud.

### Setting up Google Cloud account1.
1. Log into the console - https://console.cloud.google.com/start?tutorial=iot_core_quickstart
2. Use your personal Gmail account to log in. Select **Try for free**.
**Note:** If not, create a new email account from [HERE](https://accounts.google.com/signup/v2/webcreateaccount?hl=en&amp;flowName=GlifWebSignIn&amp;flowEntry=SignUp)
3. Create a new Google cloud project with the name – gcp-trust-demo by clicking the **Select a project**, **NEW PROJECT** and **Create**

    ![Select Project](images/gcp/select_project.png "Select Project")

    ![New Project](images/gcp/new_project.png "New Project")

    ![Create Project](images/gcp/create_project.png "Create Project")

4. Select organization if available or just select No organization
5. Once the project is created, the home page looks like the screen shot below
**Note:** Note down the Project Id which will be used later.

    ![Project Info](images/gcp/project_info.png "Project Info")


6. In the search bar, type **billing** to get to the billing page. It is necessary to do it during this step, as without credit card information, the IoT Core cannot be accessed. Click Link a billing account to add the credit card information. Follow the prompts to complete the billing information.

    ![Billing](images/gcp/billing.png "Billing")

    ![Link Billing](images/gcp/link_billing.png "Link Billing")

7. In the cloud platform search bar type **Pub/Sub API** and click on **Enable API**

    ![Enable API](images/gcp/enable_api.png "Enable API")

8. Enter **Google Cloud IoT API** in the search bar. Once you select it, click **Enable**

    ![Cloud IoT API](images/gcp/cloud_iot_api.png "Cloud IoT API")


### Creating Topic

1. In the navigational pane, select **Pub/Sub -&gt; Topics** as in the below figure

    ![Topic](images/gcp/topic.png "Topic")

2. Click Create Topic

    ![Create Topic](images/gcp/create_topic.png "Create Topic")

3. Enter the name of topic as **events** and click **Create Topic**.

    ![Creating Topic](images/gcp/creating_topic.png "Creating Topic")

### Creating Registry
1. In the navigational pane, select **IoT Core** as in the below figure

    ![IoT Core](images/gcp/iot_core.png "IoT Core")

2. Once you are inside IoT core then click on **CREATE REGISTRY**

    ![Create Registry](images/gcp/create_registry.png "Create Registry")

3. Enter the following details:
    1. Registry Id – **Name of your choice**
    2. Region – us-central1
    3. Default telemetry topic – Select the pub/sub topic you have created in the previous step from the drop down.
    4. Under SHOW ADVANCED OPTIONS
        1. Device State Topic – optional
        2. MQTT and HTTP are enabled

    5. And then click **Create**

        ![Registry Details-1](images/gcp/registry_details-1.png "Registry Details-1")

        ![Registry Details-2](images/gcp/registry_details-2.png "Registry Details-2")

4. Open *~/.trustplatform/gcp_credentials.yaml* file
    1. Enter the same Registry id entered in previous step
    2. region as us-central1 and save the file

        This file is used later in GCP connect example

        ![credentials](images/gcp/credentials.png "credentials")


### Creating Pub/Sub Service Account

1. Search for **IAM and admin** -&gt; service accounts -&gt; Create Service Account

    ![Service Account](images/gcp/service_accounts.png "Service Account")

2. Click **Create Service Account** as in below figure

    ![Create Service Account](images/gcp/create_service_account.png "Create Service Account")

3. Enter **data-view** in the service account name and click **CREATE**

    ![Data View](images/gcp/data_view.png "Data View")


4. In the next window select the role type from **Pub/Sub** as **Pub/Sub Editor** and Click **CONTINUE** as in below figures

    ![Pub/Sub](images/gcp/pub_sub.png "Pub/Sub")

    ![Pub/Sub Editor](images/gcp/pub_sub_editor.png "Pub/Sub Editor")

5. Click **DONE** for **Grant users access to this service account (optional)**
6. Click on Email link to create keys as in below

    ![Data View email](images/gcp/data_view_email.png "Data View email")

7. Click on **ADD KEY -&gt; Create new key** to create new one. In the next window make sure the JSON type is selected and Click **Create** and click **Close**

    ![Data View Key](images/gcp/data_view_key.png "Data View Key")

8. A json file is downloaded, rename the json file as **data-view.json** and place it in *~/.trustplatform/* folder.

Now we need to create another service account for the device registration through the manifest file.
### Creating Cloud IoT Service Account

1. Click **CREATE SERVICE ACCOUNT** as shown in the previous steps and enter the service account name as **iot-manifest** and click CREATE

    ![IoT Manifest](images/gcp/iot_manifest.png "IoT Manifest")


2. Select the role as **Cloud IoT Provisioner** from **Cloud IoT** and Click **CONTINUE**

    ![Cloud IoT](images/gcp/cloud_iot.png "Cloud IoT")

3. Click **DONE** for **Grant users access to this service account (optional)**
4. Click on Email link to create keys as in below

    ![IoT Manifest email](images/gcp/iot_manifest_email.png "IoT Manifest email")

5. Click on **ADD KEY -&gt; Create new key** to create new one. In the next window make sure the JSON type is selected and Click **Create** and click **Close**
6. A JSON file is downloaded and click **Done**. Rename the downloaded file as **iot-manifest.json** and place it in *~/.trustplatform/* folder.

### Creating Pub/Sub Subscription

1. Now search for **Pub/Sub** in the search bar and **Create Subscription**

    ![Pub/Sub Subscription](images/gcp/pub_sub_subscription.png "Pub/Sub Subscription")

2. Give it the name **data-view**, select a **Cloud Pub/Sub topic** as events created in the previous sections and click **CREATE**

    ![Create Subscription](images/gcp/create_subscription.png "Create Subscription")

The GCP IoT cloud account is now setup for the device registration through the manifest file.
