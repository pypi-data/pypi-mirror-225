import twine.settings


def pre(hub, ctx):
    if "ctx" in ctx.signature.parameters:
        func_ctx = ctx.args[1]
        if "acct" in func_ctx:
            func_ctx.acct.settings = twine.settings.Settings(
                non_interactive=True,
                **func_ctx.acct,
                verbose=True,
                disable_progress_bar=True,
            )
