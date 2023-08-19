import requests

from typing import Optional, List

import ujson as json
import textwrap


import logging

from clustaar.schemas.models import (
SendTextAction,
SendCardsAction,
SendQuickRepliesAction,
Card,
Button,
OpenURLAction,
StepTarget,
JumpToAction,
WaitAction
)

class Client:
    """ Class used to comunicates with the spellz api """

    def __init__(self, spellz_token: str, spellz_domain: Optional[str] = None) -> None:
        """
        Args:
            spellz_token: it corresponds to their x-api-key
            spellz_domain: the domaine (prod/staging)
        """
        self._spellz_token = spellz_token
        self._spellz_domain = spellz_domain or "https://prod-a.spellz.ai:3443"

        # TODO add quick replies extractor here when ready
        self._clustaar_extractor = {
            "text": self._extract_send_text_action,
            "cards": self._extract_send_cards_action,
            "go_to_step": self._extract_jump_to_action,
            "typing": self._extract_wait_action,
        }

        self._logger = logging.getLogger(__name__)

    def reply(self, interlocutor_id: str, message: str, session: Optional[dict] = None, extra: Optional[dict] = None) -> list:
        """
        Function used to ask a reply to the spellz bot/LLM.

        Args:
            interlocutor_id: the clustaar interlocutor id
            message: the message sended
            session: the clustaar session values
            extra: extra infos if needed
        """
        actions = []

        data = {
            "query": message,
            "sessionValues": session,
            "exrtaInfos": extra
        }

        self._logger.debug(f"Send message \"{message}\" to the spellz reply handler with interlocutor ID = {interlocutor_id}")

        res = self._post_spellz(f"/bots/interlocutor/{interlocutor_id}/interaction", data)

        if res.status_code == 200:
            json_res = res.json()
        else:
            self._logger.exception(f"Invalid status code '{res.status_code}' with reply: {res.text}")
            return []

        for s_action in json_res["actions"]:
            try:
                action = self._clustaar_extractor[s_action["type"]](s_action)
            except KeyError:
                type = s_action["type"]

                self._logger.error(f"Putain pierre pourquoi tu me passe des types pas gérés comme [\"{type}\"]!!!")

                actions.append(action)

        return actions

    def _extract_send_text_action(self, action: dict):
        """Used to extract send_text_action from spell action

        Args:
            action: an action as dict
        """
        return SendTextAction(text=action["text"], alternatives=[action["text"]])

    def _extract_wait_action(self, action: dict):
        """Used to extract wait_ction from spell action

        Args:
            action: an action as dict
        """
        return WaitAction(duration=action["duration"])

    def _extract_jump_to_action(self, action: dict):
        """Used to extract jump_to_action from spell action

        Args:
            action: an action as dict
        """
        # TODO demander a l'homme cailloux d'ajouter le name de la step dans l'action (a voir pour ajouter des connections)

        return JumpToAction(default_target=StepTarget(step_id=action["id"], name=action.get("id") or "Pierre le cailloux plat"), connections=[])

    def _extract_send_cards_action(self, action: dict):
        """Used to extract send_cards_action from spell action

        Args:
            action: an action as dict
        """
        cards = []

        for card in action["cards"]:
            buttons = []

            for button in card["buttons"]:
                title = textwrap.shorten(button["label"], 20)

                buttons.append(Button(title=title, action=OpenURLAction(url=button["value"])))

            card = Card(
                title=card["title"],
                subtitle=card["subtitle"],
                buttons=buttons,
                image_url=card.get("imageURL", ""),
                url=card.get("url", ""),
                alt=card.get("alt", "")
            )

            cards.append(card)

        return SendCardsAction(cards=cards)

    def _extract_send_quick_replies_action(self, action: dict):
        """Used to extract send_quick_replies_action from spell action

        Args:
            action: an action as dict
        """

        # TODO Wait front

        pass

    def _post_spellz(self, url: str, data: dict):
        """
        Fonction used to send an HTTP request to spellz

        Args:
            url: the targeted url point
            data: the data to send (have to be jsonifiable)
        """
        full_url = self._spellz_domain + url

        data = json.dumps(data)

        self._logger.debug(f"Send post HTTP request to \"{full_url}\" with body: {data}")

        res = requests.post(
            full_url,
            data=data,
            headers={"x-api-key": self._spellz_token, "content-type": "application/json"},
        )

        self._logger.debug(f"Successful send of a post HTTP request to \"{full_url}\" status {res.status_code} with body: {res.text}")

        return res