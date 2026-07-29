# import requests


# SEARXNG_URL = "http://localhost:8080"


# def search_searxng(query, limit=10):
#     """
#     Search using our local SearXNG instance.
#     """

#     params = {
#         "q": query,
#         "format": "json"
#     }

#     try:
#         response = requests.get(
#             f"{SEARXNG_URL}/search",
#             params=params,
#             timeout=30
#         )

#         response.raise_for_status()

#         data = response.json()

#         results = []

#         for item in data.get("results", [])[:limit]:
#             results.append({
#                 "title": item.get("title", ""),
#                 "url": item.get("url", ""),
#                 "content": item.get("content", "")
#             })

#         return results

#     except requests.RequestException as e:
#         print(f"SearXNG search failed: {e}")
#         return []


# -------------------------------------------------------------

import time
import requests


SEARXNG_URL = "http://localhost:8080/search"


def search_searxng(query, limit=10, retries=2):
    """
    Search SearXNG with basic retry and upstream-engine
    failure detection.

    Returns:
    {
        "success": bool,
        "results": list,
        "error_type": str | None,
        "unresponsive_engines": list
    }
    """

    params = {
        "q": query,
        "format": "json"
    }

    for attempt in range(retries + 1):

        try:
            response = requests.get(
                SEARXNG_URL,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            results = data.get("results", [])
            unresponsive = data.get(
                "unresponsive_engines",
                []
            )

            # Successful search
            if results:
                return {
                    "success": True,
                    "results": results[:limit],
                    "error_type": None,
                    "unresponsive_engines": unresponsive
                }

            # No results + engines failed
            if unresponsive:

                print("   SearXNG engines unavailable:")

                for engine in unresponsive:
                    if len(engine) >= 2:
                        print(
                            f"      {engine[0]} → {engine[1]}"
                        )

                # Retry only if attempts remain
                if attempt < retries:
                    wait_time = 3 * (attempt + 1)

                    print(
                        f"   Waiting {wait_time}s before retry..."
                    )

                    time.sleep(wait_time)
                    continue

                return {
                    "success": False,
                    "results": [],
                    "error_type": "SEARCH_ENGINE_UNAVAILABLE",
                    "unresponsive_engines": unresponsive
                }

            # Engines responded but genuinely no results
            return {
                "success": True,
                "results": [],
                "error_type": None,
                "unresponsive_engines": []
            }

        except requests.exceptions.ConnectionError:

            return {
                "success": False,
                "results": [],
                "error_type": "SEARXNG_CONNECTION_ERROR",
                "unresponsive_engines": []
            }

        except requests.exceptions.Timeout:

            if attempt < retries:
                wait_time = 3 * (attempt + 1)
                time.sleep(wait_time)
                continue

            return {
                "success": False,
                "results": [],
                "error_type": "TIMEOUT",
                "unresponsive_engines": []
            }

        except requests.RequestException as error:

            print(f"SearXNG request failed: {error}")

            return {
                "success": False,
                "results": [],
                "error_type": "REQUEST_ERROR",
                "unresponsive_engines": []
            }

        except ValueError:

            return {
                "success": False,
                "results": [],
                "error_type": "INVALID_JSON",
                "unresponsive_engines": []
            }