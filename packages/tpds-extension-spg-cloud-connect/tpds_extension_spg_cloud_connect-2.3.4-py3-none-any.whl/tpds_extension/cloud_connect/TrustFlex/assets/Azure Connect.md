# Trust Platform Design Suite - Usecase Help - Azure Connect

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
 - Setup Azure account. Follow the instructions at [**Azure demo account setup**](#azure-account-setup-instructions)
 - Ensure *~/.trustplatform/azure_credentials.yaml* contains the account credentials.
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
    - Set the configuration -> right click on Project, expand *Set Configuration* to select *AZURE_CONNECT*
    - Build and Program the project -> right click on Project and select *Make and Program Device*
- Log from the embedded project can be viewed using applications like TeraTerm. Select the COM port and set baud rate as 115200-8-N-1

Example TeraTerm log after successfully executing embedded project:

- Connecting to Cloud messages appear along with the led state.

![Azure Connect TeraTerm Log](images/azure_ttlog.png "Azure Connect TeraTerm Log")

## Azure Account Setup Instructions

In order to run the Azure demo an Azure account is required. This document describes the steps required to obtain and configure an Azure account for the demo.

[Azure](https://azure.microsoft.com/en-in/overview/iot/) provides computing services for a fee. Some are offered for free on a trial or small-scale basis. By signing up for your own Azure account, you are establishing an account to gain access to a wide range of computing services.

### Create your own Azure account and create IoT HUB
1. Create Azure account
    1. Go to https://portal.azure.com/ and follow instructions to create your own Azure account. If you already have an azure account, enter the credentials and log in.

2. Click **Create a resource** in the azure portal.
    ![Create Resources](images/azure/create_resources.png "Create Resources")

    If prompted for Create a Free account, Start Free account by clicking on Start Free. Once the account creation is complete, it starts over with above step. Select Create a resource again and continue with next steps.

3. Click **Internet of Things** and from that select **IoT Hub**
    ![IoT Hub](images/azure/iot_hub.png "IoT Hub")

4. The new window prompts to select the subscription, Resource Group, Region and IoT Hub Name.
    1. Select the Subscription as Free Trial.
    2. In the resource group, click Create new and enter any name of your choice.
    3. In the Region, Select any region of your choice.
    4. In the IoT Hub Name, enter a unique name to identify the Hub.

    Click Review + create after entering all the details.
    ![Review + Create](images/azure/review_create.png "Review + Create")

5. It will take you to the Review + create Tab, click Create to create an IoT Hub.
6. It will start the IoT hub deployment process and it will take a while to create the IoT hub. Once it is done it will show as the below screen.
    ![Overview](images/azure/overview.png "Overview")

7. Click Go to resource and it will take you to the IoT Hub overview page.
8. Note down only your IoT Hub Hostname(exclude .azure-devices.net) and Subscription ID as highlighted below. The Hostname should be same as one created in Step 4.4
    ![HostName](images/azure/host_name.png "HostName")

Save the credentials to azure_credentials.yaml file in ~/.trustplatform folder.