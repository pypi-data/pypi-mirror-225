#!/usr/bin/env python
import inspect
import ipaddress
import logging
import re
from datetime import datetime
import json as json_lib

import aiohttp
import asyncio

_logger = logging.getLogger("async_nec_beamer")
# Default values for the NEC Beamer
NAME = "NEC Beamer"
IP_ADDRESS = "192.168.0.175"
TIMEOUT = 5*60  # 5 minutes


class DummyResponse:
    def __init__(self, status):
        self.status = status


class Nec_Beamer:
    def __init__(self, ip_address=IP_ADDRESS, name=NAME, timeout=TIMEOUT) -> None:
        # check if ip_address is a valid IP Address (v4 and v6)
        if not ipaddress.ip_address(ip_address):
            raise ValueError("ip_address is not a valid IP Address")
        # check if name is a string
        if not isinstance(name, str):
            raise ValueError("name is not a string")
        # check if timeout is an integer
        if not isinstance(timeout, int) and timeout >= 0:
            raise ValueError("timeout is not an integer")

        self._ip_address = ip_address
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._is_on = False
        self._name = name
        self._is_available = False
        self._lamp_life_remaining = 0  # top.statusF.document.stat.textfield.value='81';
        self._lamp_hours = 0  # top.statusF.document.stat.textfield2.value='0390';
        self._filter_hours = 0  # top.statusF.document.stat.textfield4.value='0396';
        self._message_error_status = ""  # top.statusF.document.stat.textfield5.value='0000';
        self._projektor_hours_used = 0  # top.statusF.document.stat.textfield6.value='0019';

        self.__json = False

        self._muted = {
            "snd": False,
            "pic": False,
            "osd": False,
        }

        self._sources = {
            "rgb1": False,
            "rgb2": False,
            "rgb3": False,
            "comp": False,
            "vidn": False,
            "svid": False,
            "view": False,
            "lann": False,
        }

        self._commands = {
            "power_on": "/scripts/IsapiExtPj.dll?D=%05%02%00%00%00%00",
            "power_off": "/scripts/IsapiExtPj.dll?D=%05%02%01%00%00%00",
            "source_rgb1": "/scripts/IsapiExtPj.dll?D=%07%02%03%00%00%02%01%01",
            "source_rgb2": "/scripts/IsapiExtPj.dll?D=%07%02%03%00%00%02%01%02",
            "source_rgb3": "/scripts/IsapiExtPj.dll?D=%07%02%03%00%00%02%01%1A",
            "source_comp": "/scripts/IsapiExtPj.dll?D=%07%02%03%00%00%02%01%10",
            "source_vidn": "/scripts/IsapiExtPj.dll?D=%07%02%03%00%00%02%01%06",
            "source_svid": "/scripts/IsapiExtPj.dll?D=%07%02%03%00%00%02%01%0B",
            "source_view": "/scripts/IsapiExtPj.dll?D=%07%02%03%00%00%02%01%1F",
            "source_lann": "/scripts/IsapiExtPj.dll?D=%07%02%03%00%00%02%01%20",
            "bri_up": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%00%FF%01%03%00",
            "cnt_up": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%01%FF%01%03%00",
            "col_up": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%02%FF%01%03%00",
            "hue_up": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%03%FF%01%03%00",
            "shp_up": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%04%FF%01%01%00",
            "bri_dw": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%00%FF%01%FD%FF",
            "cnt_dw": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%01%FF%01%FD%FF",
            "col_dw": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%02%FF%01%FD%FF",
            "hue_dw": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%03%FF%01%FD%FF",
            "shp_dw": "/scripts/IsapiExtPj.dll?D=%0A%03%10%00%00%05%04%FF%01%FF%FF",
            # time in HHmmss
            "update": f"/scripts/IsapiExtPj.dll?S={datetime.now().strftime('%H%M%S')}",
            "mutePic": "/scripts/IsapiExtPj.dll?D=%05%02%10%00%00%00",
            "unmutePic": "/scripts/IsapiExtPj.dll?D=%05%02%11%00%00%00",
            "muteSnd": "/scripts/IsapiExtPj.dll?D=%05%02%12%00%00%00",
            "unmuteSnd": "/scripts/IsapiExtPj.dll?D=%05%02%13%00%00%00",
            "muteOSD": "/scripts/IsapiExtPj.dll?D=%05%02%14%00%00%00",
            "unmuteOSD": "/scripts/IsapiExtPj.dll?D=%05%02%15%00%00%00",
            "muteAll": "/scripts/IsapiExtPj.dll?D=ON",
            "unmuteAll": "/scripts/IsapiExtPj.dll?D=OFF",
        }

    @property
    def _selected_source(self):
        s = [k for k, v in self._sources.items() if v]
        return s[0] if s else None

    @property
    def _all_muted(self):
        return all(self._muted.values())

    @property
    def muted(self):
        return self._all_muted

    async def __send_command(self, command) -> aiohttp.ClientResponse:
        if command not in self._commands:
            _logger.error(f"Command %s not found", command)
            return
        _logger.info(f"Sending command to NEC Beamer: %s", command)
        command = self._commands[command] if command in self._commands else command
        url = f"http://{self._ip_address}{command}"
        _logger.info(f"with this URL: %s", url)

        try:
            async with aiohttp.ClientSession(timeout=self._timeout) as session:
                async with session.get(url) as response:
                    _logger.debug("Response Status: %s", response.status)
                    _logger.debug("Response Headers: %s", response.headers)
                    html = await response.text()
                    # response = requests.get(url, timeout=5)
                    _logger.debug(f"Response from NEC Beamer: %s", html[:15])
        except (aiohttp.ServerTimeoutError, aiohttp.ClientConnectorError) as e:
            _logger.error(f"Connection timed out: %s", e)
            # AttributeError: 'NoneType' object has no attribute 'status'
            # create a dummy response object with only a status attribute
            response = DummyResponse(status=408)
            return response
        self._is_available = True
        _logger.debug(f"set is_available to %s", self._is_available)
        return response

    async def __check_response_status_and_update(self, response) -> bool:
        if response.status != 200:
            _logger.error(
                f"Error sending command to NEC Beamer: %s", response.status
            )
            _logger.debug(f"  called from %s", inspect.stack()[1].function)
            return False
        html = await response.text()
        if "power_on_b.gif" and "power_off_g.gif" in html:
            self._is_on = False
        elif "power_on_g.gif" and "power_off_b.gif" in html:
            self._is_on = True
        else:
            _logger.error(f"Error updating NEC Beamer: %s", response.status)
            _logger.error("power_on*.gif not found in response.")
            if _logger.level == logging.DEBUG:
                _logger.debug(f"  called from %s", inspect.stack()[1].function)
                # get all "gif" from response.text
                all_gif = re.findall("gif", html)
                if len(all_gif) > 0:
                    _logger.debug(f"all gif from response: %s", all_gif)
                else:
                    _logger.debug(f"no gif from response\n=====================")
                    # indent the logging html output by 4 spaces
                    _logger.debug(
                        "\n".join(["HTML    " + i for i in html.split("\n")])
                    )
            return False

        # parse response.text for lamp life remaining, lamp hours, filter hours, projector hours used
        # get line from response.text that contains "top.statusF.document.stat.textfield.value= and extract the value

        if "top.statusF.document.stat.textfield.value=" in html:
            self._lamp_life_remaining = html.split(
                "top.statusF.document.stat.textfield.value="
            )[1].split(";")[0]

        # get line from response.text that contains "top.statusF.document.stat.textfield2.value= and extract the value

        if "top.statusF.document.stat.textfield2.value=" in html:
            self._lamp_hours = html.split(
                "top.statusF.document.stat.textfield2.value="
            )[1].split(";")[0]

        # get line from response.text that contains "top.statusF.document.stat.textfield4.value= and extract the value

        if "top.statusF.document.stat.textfield4.value=" in html:
            self._filter_hours = html.split(
                "top.statusF.document.stat.textfield4.value="
            )[1].split(";")[0]

        # get line from response.text that contains "top.statusF.document.stat.textfield6.value= and extract the value

        if "top.statusF.document.stat.textfield6.value=" in html:
            self._projektor_hours_used = html.split(
                "top.statusF.document.stat.textfield6.value="
            )[1].split(";")[0]

        if "top.statusF.document.stat.textfield5.value=" in html:
            self._message_error_status = html.split(
                "top.statusF.document.stat.textfield5.value="
            )[1].split(";")[0]

        # clean up values and convert to int if possible (values are like: '81')

        # get all /images/*_a.gif files and check if they are in the response.text
        # if yes this means the corresponding source is active
        # if no this means the corresponding source is not active
        # set the corresponding source to active or not active

        active_images = re.findall(r"/images/.*_a.gif", html)
        for s in self._sources:  # reset active sources
            self._sources[s] = False
        for image in active_images:
            _logger.debug(f"active image: %s", image)
            active_source_name = image.split("/")[-1].split(".")[0].split("_")[1]
            _logger.debug(f"active source name: %s", active_source_name)
            if active_source_name in self._sources:
                self._sources[active_source_name] = True
            else:
                _logger.error(f"active source name not found in sources list: %s", active_source_name)
                _logger.debug(f"image_name: %s", image)

        # <img src="./images/mute_osd_m.gif" width="100" height="30" border="0" name="mute_osd">
        for m in self._muted:  # reset muted sources
            self._muted[m] = False
        muted_images = re.findall(r"/images/.*_m.gif", html)
        for image in muted_images:
            _logger.debug(f"muted image: %s", image)
            muted_source_name = image.split("/")[-1].split(".")[0].split("_")[1]
            _logger.debug(f"muted source name: %s", muted_source_name)
            if muted_source_name in self._muted:
                self._muted[muted_source_name] = True
            else:
                _logger.error(f"muted source name not found in sources list: %s", muted_source_name)
                _logger.debug(f"image_name: %s", image)

        def __clean_value(value):
            if isinstance(value, str):
                value = value.replace("'", "").replace('"', "")
                # remove leading and trailing spaces
                value = value.strip()
            if value == "true" or value == "True":
                return True
            elif value == "false" or value == "False":
                return False
            elif isinstance(value, bool):
                return value
            elif value.isnumeric():
                return int(value)
            else:
                _logger.debug(f"unrecognized Value: %s", value)
                return value

        self._lamp_life_remaining = __clean_value(self._lamp_life_remaining)
        self._lamp_hours = __clean_value(self._lamp_hours)
        self._filter_hours = __clean_value(self._filter_hours)
        self._projektor_hours_used = __clean_value(self._projektor_hours_used)
        self._is_available = __clean_value(self._is_available)
        self._is_on = __clean_value(self._is_on)
        self._message_error_status = __clean_value(self._message_error_status)

        # if message_error_status is not "Normal operation" (or empty) log it as critical
        if self._message_error_status != "Normal operation" and self._message_error_status != "":
            _logger.critical(f"NEC Beamer has an Error status message: %s", self._message_error_status)
        return True

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    @property
    def is_available(self):
        return self._is_available

    async def turn_on(self):
        """Turn the device on."""
        response = await self.__send_command("power_on")
        _logger.debug(f"Response from NEC Beamer: %s", response)

        if response.status == 200:
            self._is_on = True
            await self.update()
        else:
            self._is_on = False
            _logger.error(f"Error turning on NEC Beamer: %s", response.status)

    async def turn_off(self):
        """Turn the device off."""
        response = await self.__send_command("power_off")

        if response.status == 200:
            await self.update()
            self._is_on = False
        else:
            self._is_on = True
            _logger.error(f"Error turning off NEC Beamer: %s", response.status)

    #    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def update(self):
        response = await self.__send_command("update")
        try:
            if response.status == 200:
                await self.__check_response_status_and_update(response)
            else:
                self._is_on = False
                self._is_available = False
                _logger.error(f"Error in updating NEC Beamer with HTTP-Status Code %s."
                              f" Beamer is not available.", response.status)
                _logger.debug(f"Response: %s", response)
                _logger.debug(f"  called from: %s", inspect.stack()[1].function)
        except AttributeError as e:
            self._is_on = False
            self._is_available = False
            _logger.error(f"Error in updating NEC Beamer. Cannot connect.")
            _logger.debug(f"AttributeError: %s", e)
            _logger.debug(f"Response: %s", response)
            _logger.debug(f"  called from: %s", inspect.stack()[1].function)

    @property
    def lamp_life_remaining(self):
        return self._lamp_life_remaining

    @property
    def lamp_hours(self):
        return self._lamp_hours

    @property
    def filter_hours(self):
        return self._filter_hours

    @property
    def projektor_hours_used(self):
        return self._projektor_hours_used

    async def source_rgb1(self):
        """Switch to VGA-Input"""
        response = await self.__send_command("source_rgb1")
        try:
            if response.status == 200:
                await self.update()
            else:
                _logger.error(f"Error switching to source_rgb1: %s", response.status)
        except AttributeError as e:
            _logger.error(f"Error in switching to source_rgb1. Cannot connect.")
            _logger.debug(f"AttributeError: %s", e)
            _logger.debug(f"Response: %s", response)

    async def source_rgb2(self):
        """Switch to BNC-Input"""
        response = await self.__send_command("source_rgb2")
        try:
            if response.status == 200:
                await self.update()
            else:
                _logger.error(f"Error switching to source_rgb2: %s", response.status)
        except AttributeError as e:
            _logger.error(f"Error in switching to source_rgb2. Cannot connect.")
            _logger.debug(f"AttributeError: %s", e)
            _logger.debug(f"Response: %s", response)

    async def source_rgb3(self):
        """Switch to DVI-Input"""
        response = await self.__send_command("source_rgb3")
        try:
            if response.status == 200:
                await self.update()
            else:
                _logger.error(f"Error switching to source_rgb3: %s", response.status)
        except AttributeError as e:
            _logger.error(f"Error in switching to source_rgb3. Cannot connect.")
            _logger.debug(f"AttributeError: %s", e)
            _logger.debug(f"Response: %s", response)

    async def source_comp(self):
        """Switch to Component-Input"""
        response = await self.__send_command("source_comp")
        try:
            if response.status == 200:
                await self.update()
            else:
                _logger.error(f"Error switching to source_comp: %s", response.status)
        except AttributeError as e:
            _logger.error(f"Error in switching to source_comp. Cannot connect.")
            _logger.debug(f"AttributeError: %s", e)
            _logger.debug(f"Response: %s", response)

    async def source_vidn(self):
        response = await self.__send_command("source_vidn")

    async def source_svid(self):
        response = await self.__send_command("source_svid")

    async def source_view(self):
        response = await self.__send_command("source_view")

    async def source_lann(self):
        response = await self.__send_command("source_lann")

    async def bri_up(self):
        response = await self.__send_command("bri_up")

    async def cnt_up(self):
        response = await self.__send_command("cnt_up")

    async def col_up(self):
        response = await self.__send_command("col_up")

    async def hue_up(self):
        response = await self.__send_command("hue_up")

    async def shp_up(self):
        response = await self.__send_command("shp_up")

    async def bri_dw(self):
        response = await self.__send_command("bri_dw")

    async def cnt_dw(self):
        response = await self.__send_command("cnt_dw")

    async def col_dw(self):
        response = await self.__send_command("col_dw")

    async def hue_dw(self):
        response = await self.__send_command("hue_dw")

    async def shp_dw(self):
        response = await self.__send_command("shp_dw")

    async def vol_up(self):
        response = await self.__send_command("vol_up")

    async def vol_dw(self):
        response = await self.__send_command("vol_dw")

    async def mute(self):
        """Mute/Unmute all output of NEC Beamer"""
        await self.update()
        if self._all_muted:
            _logger.debug(f"Unmute")
            response = await self.__send_command("unmuteAll")
        else:
            _logger.debug(f"Mute")
            response = await self.__send_command("muteAll")
        try:
            if response and response.status == 200:
                await self.update()
            else:
                _logger.error(f"Error muting All of NEC Beamer: %s", response.status)
        except AttributeError as e:
            _logger.error(f"Error muting All of NEC Beamer. Cannot connect.")
            _logger.debug(f"AttributeError: %s", e)
            _logger.debug(f"Response: %s", response)

    async def mute_picture(self):
        """Mute/Unmute Picture (and Sound?) of NEC Beamer"""
        await self.update()
        if self._muted["pic"]:
            _logger.debug(f"Unmute Picture")
            response = await self.__send_command("unmutePic")
        else:
            _logger.debug(f"Mute Picture")
            response = await self.__send_command("mutePic")
        try:
            if response.status == 200:
                await self.update()
            else:
                _logger.error(f"Error muting Picture of NEC Beamer: %s", response.status)
        except AttributeError as e:
            _logger.error(f"Error muting Picture of NEC Beamer. Cannot connect.")
            _logger.debug(f"AttributeError: %s", e)
            _logger.debug(f"Response: %s", response)

    async def mute_osd(self):
        """Mute/Unmute OSD of NEC Beamer"""
        await self.update()
        if self._muted["osd"]:
            _logger.debug(f"Unmute OSD")
            response = await self.__send_command("unmuteOSD")
        else:
            _logger.debug(f"Mute OSD")
            response = await self.__send_command("muteOSD")
        try:
            if response.status == 200:
                await self.update()
            else:
                _logger.error(f"Error muting OSD of NEC Beamer: %s", response.status)
        except AttributeError as e:
            _logger.error(f"Error muting OSD of NEC Beamer. Cannot connect.")
            _logger.debug(f"AttributeError: %s", e)
            _logger.debug(f"Response: %s", response)

    async def mute_audio(self):
        """Mute/Unmute Audio of NEC Beamer"""
        await self.update()
        if self._muted["snd"]:
            _logger.debug(f"Unmute Audio")
            response = await self.__send_command("unmuteSnd")
        else:
            _logger.debug(f"Mute Audio")
            response = await self.__send_command("muteSnd")
        try:
            if response.status == 200:
                await self.update()
            else:
                _logger.error(f"Error muting Audio of NEC Beamer: %s", response.status)
        except AttributeError as e:
            _logger.error(f"Error muting Audio of NEC Beamer. Cannot connect.")
            _logger.debug(f"AttributeError: %s", e)
            _logger.debug(f"Response: %s", response)

    def __repr__(self) -> str:
        return f"Nec_Beamer(\'{self._ip_address}\', \'{self._name}\')"

    def __str__(self) -> str:
        if self.__json:
            return f"{self.__json_dict()}"
        else:
            return f"{self.__text()}"

    def __json_dict(self) -> dict:
        """Returns the status of the beamer in a JSON format"""
        try:
            selected_source = [key for key, value in self._sources.items() if value is True][0]
        except IndexError:
            selected_source = None

        json_dict = {
            "name": self._name,
            "ip_address": self._ip_address,
            "is_on": self._is_on,
            "is_available": self._is_available,
            "status": {
                "lamp_life_remaining": self._lamp_life_remaining,
                "lamp_hours": self._lamp_hours,
                "filter_hours": self._filter_hours,
                "projektor_hours_used": self._projektor_hours_used,
                "error_status": self._message_error_status,
            },
            "muted": self._muted,
            "selected-source": selected_source,
        }
        return json_dict

    def __text(self):
        """Prints the status of the beamer in a human-readable format"""
        return f"""Name: {self._name}
IP Address: {self._ip_address}
Is On: {self._is_on}
Is Available: {self._is_available}
    Lamp Life Remaining: {self._lamp_life_remaining}
    Lamp Hours: {self._lamp_hours}
    Filter Hours: {self._filter_hours}
    Projektor Hours Used: {self._projektor_hours_used}
    Message: {self._message_error_status}
Is Muted All: {self._all_muted}
    Is Muted Picture: {self._muted["pic"]}
    Is Muted OSD: {self._muted["osd"]}
    Is Muted Audio: {self._muted["snd"]}
Selected Source: {self._selected_source}"""

    def print_status(self, json=False):
        """Prints the status of the beamer in a human-readable format or in a JSON format"""
        if json or self.__json:
            print(json_lib.dumps(self.__json_dict(), indent=4))
            _logger.debug(json_lib.dumps(self.__json_dict(), indent=4, sort_keys=True))
            return
        print(self.__text())
        _logger.debug(self.__text())
