"""Config flow for Renson Healthbox integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol


from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from homeassistant.const import CONF_HOST, CONF_API_KEY

from .const import DOMAIN, LOGGER
from pyhealthbox3.healthbox3 import (
    Healthbox3,
    Healthbox3ApiClientAuthenticationError,
    Healthbox3ApiClientCommunicationError,
    Healthbox3ApiClientError,
)

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Renson Healthbox."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                if CONF_API_KEY in user_input:
                    await self._test_credentials(
                        ipaddress=user_input[CONF_HOST],
                        apikey=user_input[CONF_API_KEY],
                    )
                else:
                    await self._test_connectivity(ipaddress=user_input[CONF_HOST])
            except Healthbox3ApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                errors["base"] = "auth"
            except Healthbox3ApiClientCommunicationError as exception:
                LOGGER.error(exception)
                errors["base"] = "connection"
            except Healthbox3ApiClientError as exception:
                LOGGER.exception(exception)
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(f"{DOMAIN}_{user_input[CONF_HOST]}")
                return self.async_create_entry(
                    title=user_input[CONF_HOST],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(CONF_HOST),
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
            errors=errors,
        )

    async def _test_credentials(self, ipaddress: str, apikey: str) -> None:
        """Validate credentials."""
        client = Healthbox3(
            host=ipaddress,
            api_key=apikey,
            session=async_create_clientsession(self.hass),
        )
        await client.async_enable_advanced_api_features()

    async def _test_connectivity(self, ipaddress: str) -> None:
        """Validate connectivity."""
        client = Healthbox3(
            host=ipaddress,
            api_key=None,
            session=async_create_clientsession(self.hass),
        )
        await client.async_validate_connectivity()


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
