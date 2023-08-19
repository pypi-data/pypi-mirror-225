""""
Unofficial Anchor API connector.

This package allows you to fetch data from the inofficial Anchor Podcast API.
The API is not documented and may change at any time. Use at your own risk.
"""
from typing import Any, Dict, Iterator, Optional
from datetime import datetime
from threading import RLock
import requests

DELAY_BASE = 2.0
MAX_REQUEST_ATTEMPTS = 6


class AnchorConnector:
    """Representation of the unofficial Anchor podcast API."""

    def __init__(self, base_url, webstation_id, anchorpw_s):
        """
        Initializes the AnchorConnector object.

        Args:
            base_url (str): Base URL for the API.
            webstation_id (str): Anchor Podcast ID for the API
            anchorpw_s (str): Anchor API token (from anchorpw_s cookie)
        """

        self.base_url = base_url
        self.webstation_id = webstation_id
        self.cookies = {"anchorpw_s": anchorpw_s}
        self._auth_lock = RLock()

    def _build_url(self, *args) -> str:
        return f"{self.base_url}/{'/'.join(args)}"

    def _date_params(self, start: datetime, end: datetime) -> Dict[str, str]:
        return {
            "timeRangeStart": str(int(start.timestamp())),
            "timeRangeEnd": str(int(end.timestamp())),
        }

    def _request(self, url: str, parms: Optional[dict] = None) -> dict:
        response = requests.get(
            url,
            params=parms,
            cookies=self.cookies,
            timeout=60,  # in seconds
        )

        if response.status_code == 200:
            return response.json()
        return response.raise_for_status()

    def audience_size(self) -> dict:
        """
        Loads audience size data.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "audienceSize",
        )
        return self._request(url)

    def episodes(
        self,
        is_mums_compatible: bool = True,
        limit: int = 15,
        order_by: str = "publishOn",
        page_token: Optional[str] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Loads podcast episode data.

        Returns an iterator over all episodes.

        Args:
            is_mums_compatible (bool): Indicates if the episodes are MUMS compatible.
            limit (int): Number of results per page.
            order_by (str): Sort by field.
            page_token (Optional[str], optional): Page token for pagination.
              Defaults to None.

        Returns:
            (Iterator[Dict[str, Any]]): Episode iterator.
        """

        total = 0

        while True:
            response = self._episode_page(
                is_mums_compatible, limit, order_by, page_token
            )

            for episode in response["items"]:
                if total >= limit:
                    # We've reached the limit, so stop
                    return

                yield episode
                total = total + 1

            if response.get("next") is None:
                break

            page_token = (
                response["next"].split("pageToken=")[-1] if response["next"] else None
            )

    def _episode_page(
        self,
        is_mums_compatible: bool,
        limit: int,
        order_by: str,
        page_token: Optional[str] = None,
    ) -> dict:
        """
        Internal method.
        Loads a single page of podcast episode data.
        """

        # Note:
        # "stations" is no typo here. It's the only API endpoint with this prefix.
        # All other endpoints use "station".
        url = self._build_url(
            "stations", format(f"webStationId:{self.webstation_id}"), "episodePage"
        )
        params = {
            "isMumsCompatible": str(is_mums_compatible).lower(),
            "limit": str(limit),
            "orderBy": order_by,
        }
        if page_token:
            params["pageToken"] = page_token
        return self._request(url, params)

    def plays(
        self, start: datetime, end: datetime, time_interval: int = 86_400
    ) -> dict:
        """
        Loads plays data.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "plays",
        )
        params = {"timeInterval": str(time_interval), **self._date_params(start, end)}
        return self._request(url, params)

    def plays_by_age_range(self, start: datetime, end: datetime) -> dict:
        """
        Shows the number of plays by age range.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "playsByAgeRange",
        )
        params = self._date_params(start, end)
        return self._request(url, params)

    def plays_by_app(
        self, start: datetime, end: datetime, user_id: Optional[int] = None
    ) -> dict:
        """
        Shows the number of plays by app (optionally for a given user).
        The user ID is optional but it is relevant because it has an impact on
        the response.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "playsByApp",
        )

        params = self._date_params(start, end)
        if user_id:
            params["userId"] = str(user_id)

        return self._request(url, params)

    def plays_by_device(
        self, start: datetime, end: datetime, user_id: Optional[int] = None
    ) -> dict:
        """
        Shows the number of plays by device (optionally for a given user).
        The user ID is optional but it is relevant because it has an impact on
        the response.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "playsByDevice",
        )

        params = self._date_params(start, end)
        if user_id:
            params["userId"] = str(user_id)

        return self._request(url, params)

    def plays_by_episode(
        self,
        start: datetime,
        end: datetime,
        time_interval: int = 86_400,
        limit: Optional[int] = None,
    ) -> dict:
        """
        List of episodes, ranked by number of plays.
        It is used to show the most played episodes on the Anchor dashboard.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "playsByEpisode",
        )
        params = {
            "timeInterval": str(time_interval),
            **self._date_params(start, end),
        }
        if limit:
            params["limit"] = str(limit)

        return self._request(url, params)

    def plays_by_gender(self, start: datetime, end: datetime) -> dict:
        """
        Get the number of plays by gender
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "playsByGender",
        )
        params = self._date_params(start, end)
        return self._request(url, params)

    def plays_by_geo(self, limit: int = 200) -> dict:
        """
        Get the number of plays by country for the webstation.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "playsByGeo",
        )
        # `resultGeo=geo2` returns country data.
        params = {"limit": str(limit), "resultGeo": "geo2"}
        return self._request(url, params)

    def plays_by_geo_city(self, country: str, limit: int = 200) -> dict:
        """
        Get the number of plays by city for the webstation.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "playsByGeo",
        )
        params = {"limit": str(limit), "resultGeo": "geo3", "geo2": country}
        return self._request(url, params)

    def podcast_episode(self) -> dict:
        """
        Get the podcast episodes for the webstation.
        This is an outlier in the API, as it's not a sub-endpoint of the station.
        The URL is hardcoded here, as it doesn't follow the usual pattern and
        is only used once.
        """
        url = "https://podcasters.spotify.com/pod/api/podcastepisode"
        return self._request(url)

    def total_plays(self, is_mums_compatible: bool) -> dict:
        """
        Loads total plays data.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "totalPlays",
        )
        params = {"isMumsCompatible": str(is_mums_compatible).lower()}
        return self._request(url, params)

    def total_plays_by_episode(self) -> dict:
        """
        Loads total plays by episode
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "totalPlaysByEpisode",
        )
        return self._request(url)

    def unique_listeners(self) -> dict:
        """
        Loads unique listeners data.
        """
        url = self._build_url(
            "analytics",
            "station",
            format(f"webStationId:{self.webstation_id}"),
            "uniqueListeners",
        )
        return self._request(url)

    def episode_plays(
        self,
        web_episode_id: str,
        start: datetime,
        end: datetime,
        time_interval: str = "daily",
    ) -> dict:
        """Loads plays data for a specific episode.

        Args:
            web_episode_id (str): ID of the episode to request data for.

        Returns:
            dict: Response data from API.
        """
        url = self._build_url(
            "analytics", "episode", format(f"webEpisodeId:{web_episode_id}"), "plays"
        )
        params = self._date_params(start, end)

        if time_interval == "weekly":
            params["timeInterval"] = "604800"
        elif time_interval == "monthly":
            params["timeInterval"] = "2628000"
        else:
            params["timeInterval"] = "86400"

        return self._request(url, params)

    def episode_performance(self, web_episode_id: str) -> dict:
        """Loads performance data for a specific episode.

        Args:
            web_episode_id (str): ID of the episode to request data for.

        Returns:
            dict: Response data from API.
        """
        url = self._build_url(
            "analytics",
            "episode",
            format(f"webEpisodeId:{web_episode_id}"),
            "performance",
        )
        return self._request(url)

    def episode_aggregated_performance(self, web_episode_id: str) -> dict:
        """Loads aggregated performance data for a specific episode.

        Args:
            web_episode_id (str): ID of the episode to request data for.

        Returns:
            dict: Response data from API.
        """
        url = self._build_url(
            "analytics",
            "episode",
            format(f"webEpisodeId:{web_episode_id}"),
            "aggregatedPerformance",
        )
        return self._request(url)

    def episode_all_time_video_data(self, episode_id: str) -> dict:
        """
        Loads all time video data for a specific episode.
        """
        url = self._build_url("analytics", "episode", episode_id, "allTimeVideoData")
        return self._request(url)
