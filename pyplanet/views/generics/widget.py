import logging

from asyncio import iscoroutinefunction

from pyplanet.apps.core.maniaplanet.models import Player
from pyplanet.views.template import TemplateView

logger = logging.getLogger(__name__)


class WidgetView(TemplateView):
	widget_x = None
	widget_y = None
	size_x = None
	size_y = None
	title = None
	icon_style = None
	icon_substyle = None

	action = None

	template_name = 'core.views/generics/widget.xml'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Setup the receivers.
		self.subscribe('open_widget', self.open_widget)

	async def open_widget(self, player, action, values, **kwargs):
		if self.action is not None:
			# Execute action/target method.
			if iscoroutinefunction(self.action):
				await self.action(player)
			else:
				self.action(player)

	async def close(self, player, *args, **kwargs):
		"""
		Close the link for a specific player. Will hide manialink and destroy data for player specific to save memory.

		:param player: Player model instance.
		:type player: pyplanet.apps.core.maniaplanet.models.Player
		"""
		if self.player_data and player.login in self.player_data:
			del self.player_data[player.login]
		await self.hide(player_logins=[player.login])

	async def refresh(self,  player=None, *args, **kwargs):
		"""
		Refresh list with current properties for a specific player. Can be used to show new data changes.

		:param player: Player model instance.
		:type player: pyplanet.apps.core.maniaplanet.models.Player
		"""
		await self.display(player=player)

	async def display(self, player=None):
		"""
		Display list to player.

		:param player: Player login or model instance.
		:type player: str, pyplanet.apps.core.maniaplanet.models.Player
		"""
		login = player.login if isinstance(player, Player) else player
		if not player:
			return await super().display()
		return await super().display(player_logins=[login])

	async def get_title(self):
		return self.title

	async def get_context_data(self):
		context = await super().get_context_data()

		icon_x = 0.5
		title_x = 5.5
		title_halign = 'left'
		if self.widget_x < 0:
			icon_x = (self.size_x - 2.5 - 4.5)
			title_x = (icon_x - 0.5)
			title_halign = 'right'

		hover_color = '3341'
		if self.action is not None:
			hover_color = '09F4'

		# Add facts.
		context.update({
			'widget_x': self.widget_x,
			'widget_y': self.widget_y,
			'size_x': self.size_x,
			'size_y': self.size_y,
			'hover_color': hover_color,
			'icon_x': icon_x,
			'title': await self.get_title(),
			'title_x': title_x,
			'title_halign': title_halign,
			'open_action': (self.action is not None),
			'icon_style': self.icon_style,
			'icon_substyle': self.icon_substyle
		})

		return context
