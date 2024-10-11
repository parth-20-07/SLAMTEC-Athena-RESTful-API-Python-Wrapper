from typing import List, Dict


class robotComms:

    # Constructors
    def __init__(self, run_remote_url: bool = False, remote_url: str = '') -> None:
        if not run_remote_url:
            print("Communication Instantiated via Local URL")
            self.CURRENT_URL = self._LOCAL_URL
            self._reindex_api()
            print(f"Communication Initiated in Local Network at: {self._LOCAL_URL}")
        else:
            print("Communication Instantiated via Remote URL")
            self._REMOTE_URL = self.set_new_url(remote_url)
            self.CURRENT_URL = self._REMOTE_URL
            self._reindex_api()
            print(f"Communication Initiated in Remote Network at: {self._REMOTE_URL}")

    # Public Methods
    def set_new_url(self, new_url: str = '') -> str:
        # Get Input for Remote URL
        if (new_url == ''):
            print("URL Not Provided.")
            while (new_url == ''):
                new_url: str = input("Please Enter New URL: ")
                new_url = self.santize_url(new_url)
                confirmation: str = input(f"Confirm New URL: {new_url}? (y/n)")
                if (confirmation != 'y'):
                    print("Try Again")
                    new_url = ''
        else:
            new_url = self.santize_url(new_url)
        print(f"URL Confirmed: {new_url}")
        return new_url


    # Private Methods
    def _reindex_api(self) -> None:
        for plugin in self._plugins:
            for feature in self._feature[plugin]:
                for resource in self._resources[feature]:
                    print(f"{self.CURRENT_URL}/api/{plugin}/{feature}/{resource}")
    # Static Methods

    @staticmethod
    def santize_url(url: str) -> str:
        # Check for http in Remote URL
        http_check: str = url[0:7]
        if (http_check != 'http://'):
            url = "http://" + url
        return url

    # Class Variables
    _LOCAL_URL: str = "http://192.168.11.1:1448"

    def get_local_url(self) -> str:
        return self._LOCAL_URL

    def set_local_url(self, url: str = '') -> None:
        self._LOCAL_URL = self.set_new_url(url)
        print(f"Communication Initiated in Local Network at: {self._LOCAL_URL}")

    _REMOTE_URL: str = ""

    def get_remote_url(self) -> str:
        return self._REMOTE_URL

    def set_remote_url(self, url: str = '') -> None:
        self._REMOTE_URL = self.set_new_url(url)
        print(f"Communication Initiated in Remote Network at: {self._REMOTE_URL}")

    _VERSION_NUM: str = "/v1"

    # API Interfaces
    _plugins: List[str] = ["core", "platform", "multi_floor_map", "delivery"]
    _feature = {
        "core": [
            "system",
            "slam",
            "artifact",
            "motion",
            "firmware",
            "statistics",
            "sensors",
            "application"],
        "platform": [],
        "multi_floor_map": [],
        "delivery": []
    }
    _resources = {
        "system": [
            "capabilities",
            "power/status",
            "power/:shutdown",
            "power/:hibernate",
            "power/:wakeup",
            "power/:restartmodule",
            "robot/info"
        ],
        "slam": [
            "localization/pose",
            "localization/odopose",
            "localization/quality"
        ]
    }


def main():
    r1 = robotComms()
    r1.core_system()


if __name__ == "__main__":
    main()
