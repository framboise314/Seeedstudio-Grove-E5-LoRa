# Seeedstudio-Grove-E5-LoRa
Grove E5 LoRa board connected to a Raspberry Pi 400 - Programs Python
![Lora_E5_Seeedstudio_FB](https://user-images.githubusercontent.com/5877909/169697438-0d9698fd-550e-4186-b74a-ba70e8bb718b.jpg)

Well on my way to refurbish the LoRa gateway on TTN (previous article) I received from SeeedStudio -for testing- their LoRaWan Grove E5 board. My idea in the future would be to couple it (in two words) with a Raspberry Pi PICO to make a low cost and low power IoT. Thanks to those who remind me at each article of the same kind that you can do it with an Arduino or an ESP, but my choice is the Raspberry Pi family and so I develop my projects with the Raspberry Pi 😛 I reassure you, I do stuff with Arduino too ! After the blog pages are open and if you want to publish your Arduino projects, they are welcome! We are not chauvinistic 😆

![Lora_E5_Seeedstudio_21](https://user-images.githubusercontent.com/5877909/169697482-1b12f061-1fea-497d-beca-3fdd2881ce33.jpg)

The board is in a closed bag, with a Grove cable that allows you to connect it directly to a Grove Arduino shield, a Pico Grove or other... In my case, I will simply use this Grove plug to connect Dupont wires and link the LoRa E5 board to the GPIOs of the Raspberry Pi 400. (In black under the bag is an electronics engineer's T-shirt with a transistor flocked on it. Thanks SeeedStudio for this goody). The module is driven via the serial port with AT commands.

![Lora_E5_Seeedstudio_22](https://user-images.githubusercontent.com/5877909/169697511-0aeffe60-b7c9-4388-b324-391a54b58370.jpg)

The board has few components. On the left is the Grove socket, in the centre is the LoRa-E5 circuit and on the right is the built-in antenna which is a coiled wire. There is also a UFL socket marked ANT in the front left corner. This socket is used to connect a "real" antenna or a SMA UFL adapter to be attached to a cabinet. Please note: this type of socket is not designed to be permanently connected or disconnected! The number of connections/disconnections of the antenna must be kept to a minimum, otherwise the connector will be damaged...

![loranode](https://user-images.githubusercontent.com/5877909/169697544-fd148a1a-70ff-4512-b4e3-6d7f074a602d.jpg)

I couldn't find any info on simultaneously connecting an antenna to the UFL connector while already having an on-board antenna... A priori I'd say it's one or the other but I'll try to get the info via a contact at SeeedStudio.

Demo video here :
https://youtu.be/3-31LQ4aA5Y

More informations : https://www.framboise314.fr/carte-seeedstudio-lora-grove-e5/

