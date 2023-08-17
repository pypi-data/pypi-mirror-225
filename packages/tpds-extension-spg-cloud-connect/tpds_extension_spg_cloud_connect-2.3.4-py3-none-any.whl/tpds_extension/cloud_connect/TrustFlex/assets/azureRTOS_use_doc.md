## Trust Platform Design Suite - Usecase Help - Azure RTOS
### Overview

This page will guide you through the process of connecting a single device to Azure IoT services using individual enrollment with the ECC608B pre-provisioned certificate. This involves setting up the development environment, covering instructions for Azure DPS creation, and monitoring sample telemetry messages once the device is registered.

###Development environment Setup

Please download and install MPLAB X IDE V6.00, MPLAB Harmony V3 and MPLAB X32 Compiler

- Download and install MPLAB X: 
[https://microchipdeveloper.com/install:mplabx](https://microchipdeveloper.com/install:mplabx)
- Download and install MPLAB X32 Compiler: 
[https://microchipdeveloper.com/install:xc32](https://microchipdeveloper.com/install:xc32)
- Download and install MPLAB Harmony: 
[https://microchipdeveloper.com/harmony3:mhc-overview#install](https://microchipdeveloper.com/harmony3:mhc-overview#install)



### Hardware setup

This section details the hardware setup to run this demo and requires the use of the following equipment parts:

- The [SAM E54 Xplained Pro evaluation kit](https://www.microchip.com/en-us/development-tool/atsame54-xpro)
- The [ATECC608B-TFLXTLS secure element](https://www.microchip.com/en-us/product/ATECC608B-TFLXTLS)
- The [Mikrobus Xplained Proadapter](https://www.microchip.com/en-us/development-tool/ATMBUSADAPTER-XPRO)

Please connect the ATECC608b-TFLXTLS to the ATSAME54-XPRO board and set the connection to the **EXT1** of the board.

Set the switches of the ATECC608b to select TNGTLS/TFLXTLS as shown in Figure-2.

You will also need an Ethernet connection to connect the device to Azure IoT Hub services later.

<figure>
<img src="images/azureRTOS/SAME54_connection.png" alt="Figure-1"  width="500">
<figcaption>Figure-1. SAM54 and ATECC608b connection </figcaption>
</figure>

<figure>
<img src="images/azureRTOS/ATECC_switch.png" alt="Figure-2" width="300"> 
<figcaption>Figure-2. **Switch setup**</figcaption>
</figure>
<p>&nbsp;</p>

### Usecase configuration:

**1. MPLAB X Path:**

Once MPLAB X is installed on your machine, you need to note down the Path and set it in TPDS system settings.

- Go to _File_ -\> _Preference_ then _System Settings._

This helps to program the Usecase prototyping kit to factory reset application and to access the embedded project.

 **2. Azure credentials:**

All your Azure credentials and IoT hub information shall be saved in the_azure\_credentials.yaml_file located in _**~/.trustplatform**_ folder, where ~ indicates your home directory.

- On Windows home directory is usually \user\username
- On Mac it's /users/username
- On Linux/Unix home directory is /home/username

 **3. Usecase working directory**

You can find the Usecase working directory under _**~/.trustplatform /spg\_cloud\_connect**_. It contains all the resources generated during transaction diagram execution.
<p>&nbsp;</p>

### Azure IoT Setup and DPS configuration

**1. Azure account setup**

To run this Azure IoT connectivity sample, you will need an Azure account along with a valid **subscription** to access the different IoT hub services that Azure provides.

Microsoft Azure usually provides cloud computing services for a fee, however some are offered for free on a trial or small-scale basis.

You can [create a free account](https://azure.microsoft.com/en-ca/free/) and set up a free trial subscription if you don't have one before you begin.

Please refer to this [page](https://azure.microsoft.com/en-ca/pricing/) for more information about the different plans available and the pricing options.

If you already have an account with an **active** subscription, please skip the next section.
<br>

TPDS manages your device connection and enrollment to the [IoT Hub Device Provisioning Service (DPS)](https://docs.microsoft.com/azure/iot-dps/), in a simple and easy manner.

To get started, you will need your account credentials to log in, and to note down your **Subscription ID**.

Simply navigate to the Azure portal page and click on "Subscriptions".
<br>
<figure>
<img src="images/azureRTOS/azure_portal.png" alt="Figure-3" >
<figcaption>Figure-3. Azure Portal </figcaption>
</figure>
<p>&nbsp;</p>
<figure>
<img src="images/azureRTOS/azure_subscription.png" alt="Figure-4" > 
<figcaption>Figure-4. Azure Susbcription</figcaption>
</figure>
<br>

**2. Resource Group & IoT Hub creation**

To enroll your device to DPS, an IoT Hub instance needs to be created. For this, you will be choosing a name for the **Resource group**, selecting a **Region**, and choosing a **name** for yourIoT Hub. The name needs to be **globally unique**.
It should be noted that the Hub creation process may take a moment, so please wait, and try not to interrupt it. for further information about the hub creation, please refer to this page.
<br>
<figure>
<img src="images/azureRTOS/azure_resource.png" alt="Figure-5" >
<figcaption>Figure-5. Resource group creation </figcaption>
</figure>
<p>&nbsp;</p>
<figure>
<img src="images/azureRTOS/azure_hub_create.png" alt="Figure-6" > 
<figcaption>Figure-6. IoT Hub creation</figcaption>
</figure>
<br>


**3. DPS creation and device enrollment**

Azure [IoT Hub Device Provisioning Service](https://docs.microsoft.com/azure/iot-dps/) is a helper service for IoT Hub that provides all the means to provision devices in a secure and scalable manner.
Once the IoT Hub is set, a DPS instance shall be created and linked to this Hub. You can enter any **name** of your choice for this to take place. Please note that only alphanumeric characters are accepted.

<figure>
<img src="images/azureRTOS/dps.png" alt="Figure-7" >
<figcaption>Figure-7. DPS creation </figcaption>
</figure>
<br>

Now the last step is to enroll the device to the DPS instance previously created. The X.509 certificate authentication mechanism is used for this use case connectivity sample.
TPDS manages the enrollment process by first generating the provisioned certificate and registering the device. Your device will be identified by its certificate's **Common Name.**
The Azure RTOS application running on your SAM-E54 board, is expecting two configuration parameters to connect your device to the cloud: **idScope** & **Device\_id**.
The _idScope_ is generated by Azure once the DPS instance is created. It refers to uniquely identifying the specific provisioning service where your device is registered. _Device\_id_ simply refers to the certificate's common name.

You can always check and manage your device enrollment details on the Azure portal page. Simply click on your DPS instance previously created and go to "Manage enrollments" as shown in teh folloning figure.

<figure>
<img src="images/azureRTOS/azure_enroll.png" alt="Figure-8" >
<figcaption>Figure-8. Azure Manage enrollments  </figcaption>
</figure>
<br>

TPDS eases the process of providing the AzureRTOS application with the idScope and Device\_id values required for the device connectivity configuration.
The ATECC608B possesses 16 slots that are configured for different use cases.
The idScope is saved in **Slot 8** as it is the slot configured for being used for general purpose data storage, and shall be fetched later by the MCU after **resetting** the board. Device\_id is also taken care of by the firmware running on the microcontroller.
<p>&nbsp;</p>

### Board Reset & Telemetry messages preview

This AzureRTOS demo connectivity sample is almost set. Please push the **Reset** button of your board and make sure it's connected to internet via the Ethernet cable.
Now to watch the IoT telemetry sample messages, you've got the choice of using either of these two methods:
- Serial console connection (Target USB)
- Setting up Azure IoT Explorer or IoT Central
<br>

**1. Serial Console method:**

The SAM E54 Xplained Pro has a USB Micro-AB connector for use with the USB module labeled as **TARGET USB** on the kit. Connect the board using a micro USB cable and use a console application of your choice to monitor outputs from the terminal.

<figure>
<img src="images/azureRTOS/same54_all_conn.jpg" width= "400" alt="Figure-9" >
<figcaption>Figure-9. ATSAME54-XPRO Target USB connection  </figcaption>
</figure>
<br>

This is what you should see on the console.

<figure>
<img src="images/azureRTOS/console_prints.png" width= "400" alt="Figure-10" >
<figcaption>Figure-10. Console outputs & Telemetry messages </figcaption>
</figure>
<br>

**2. Azure IoT Explorer:**

Azure IoT Explorer is a tool that provides full interaction with your connected devices. You can monitor all messages sent, test and modify your device properties and run commands. To use this tool, go to [Azure IoT explorer releases](https://github.com/Azure/azure-iot-explorer/releases), and install the latest version.
Once set, log in with your usual Azure credentials and navigate to IoT hubs. You should see your Device ID relative to the DPS instance previously created.

<figure>
<img src="images/azureRTOS/azure_iotexplore.png" width= "500" alt="Figure-11" >
<figcaption>Figure-11. Console outputs & Telemetry messages </figcaption>
</figure>
