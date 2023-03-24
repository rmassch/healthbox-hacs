"""Adds config flow for Blueprint."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_IP_ADDRESS, CONF_API_KEY
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    Healthbox3ApiClient,
    Healthbox3ApiClientAuthenticationError,
    Healthbox3ApiClientCommunicationError,
    Healthbox3ApiClientError,
)
from .const import DOMAIN, LOGGER


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                if CONF_API_KEY in user_input:
                    await self._test_credentials(
                        ipaddress=user_input[CONF_IP_ADDRESS],
                        apikey=user_input[CONF_API_KEY],
                    )
                else:
                    await self._test_connectivity(ipaddress=user_input[CONF_IP_ADDRESS])
            except Healthbox3ApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except Healthbox3ApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except Healthbox3ApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_IP_ADDRESS],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_IP_ADDRESS,
                        default=(user_input or {}).get(CONF_IP_ADDRESS),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Optional(CONF_API_KEY): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _test_credentials(self, ipaddress: str, apikey: str) -> None:
        """Validate credentials."""
        client = Healthbox3ApiClient(
            ipaddress=ipaddress,
            apikey=apikey,
            session=async_create_clientsession(self.hass),
        )
        await client.async_enable_advanced_api_features()

    async def _test_connectivity(self, ipaddress: str) -> None:
        """Validate connectivity."""
        client = Healthbox3ApiClient(
            ipaddress=ipaddress,
            apikey=None,
            session=async_create_clientsession(self.hass),
        )
        await client.async_validate_connectivity()
