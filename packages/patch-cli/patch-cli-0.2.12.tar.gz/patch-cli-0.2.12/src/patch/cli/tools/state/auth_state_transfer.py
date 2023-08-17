from patch.cli.tools.state.bi_directional_state_transfer import BiDirectionalStateTransfer

class AuthStateTransfer(BiDirectionalStateTransfer):
    def __init__(self, patch_context, path, path_poll):
        super().__init__(patch_context, path, path_poll)
