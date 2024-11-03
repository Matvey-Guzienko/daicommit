from ..i18n import Language, i18n

from .config import get_config
from .removeConventionalCommitWord import remove_conventional_commit_word

global_config = get_config()
translation = i18n[global_config['LANGUAGE'] or 'en']

IDENTITY = 'You are to act as an author of a commit message in git.'

GITMOJI_HELP = """Use GitMoji convention to preface the commit. Here are some help to choose the right emoji (emoji, description): 
🐛, Fix a bug; 
✨, Introduce new features; 
📝, Add or update documentation; 
🚀, Deploy stuff; 
✅, Add, update, or pass tests; 
♻️, Refactor code; 
⬆️, Upgrade dependencies; 
🔧, Add or update configuration files; 
🌐, Internationalization and localization; 
💡, Add or update comments in source code;"""

FULL_GITMOJI_SPEC = f"""{GITMOJI_HELP}
🎨, Improve structure / format of the code; 
⚡️, Improve performance; 
🔥, Remove code or files; 
🚑️, Critical hotfix; 
💄, Add or update the UI and style files; 
🎉, Begin a project; 
🔒️, Fix security issues; 
🔐, Add or update secrets; 
🔖, Release / Version tags; 
🚨, Fix compiler / linter warnings; 
🚧, Work in progress; 
💚, Fix CI Build; 
⬇️, Downgrade dependencies; 
📌, Pin dependencies to specific versions; 
👷, Add or update CI build system; 
📈, Add or update analytics or track code; 
➕, Add a dependency; 
➖, Remove a dependency; 
🔨, Add or update development scripts; 
✏️, Fix typos; 
💩, Write bad code that needs to be improved; 
⏪️, Revert changes; 
🔀, Merge branches; 
📦️, Add or update compiled files or packages; 
👽️, Update code due to external API changes; 
🚚, Move or rename resources (e.g.: files, paths, routes); 
📄, Add or update license; 
💥, Introduce breaking changes; 
🍱, Add or update assets; 
♿️, Improve accessibility; 
🍻, Write code drunkenly; 
💬, Add or update text and literals; 
🗃️, Perform database related changes; 
🔊, Add or update logs; 
🔇, Remove logs; 
👥, Add or update contributor(s); 
🚸, Improve user experience / usability; 
🏗️, Make architectural changes; 
📱, Work on responsive design; 
🤡, Mock things; 
🥚, Add or update an easter egg; 
🙈, Add or update a .gitignore file; 
📸, Add or update snapshots; 
⚗️, Perform experiments; 
🔍️, Improve SEO; 
🏷️, Add or update types; 
🌱, Add or update seed files; 
🚩, Add, update, or remove feature flags; 
🥅, Catch errors; 
💫, Add or update animations and transitions; 
🗑️, Deprecate code that needs to be cleaned up; 
🛂, Work on code related to authorization, roles and permissions; 
🩹, Simple fix for a non-critical issue; 
🧐, Data exploration/inspection; 
⚰️, Remove dead code; 
🧪, Add a failing test; 
👔, Add or update business logic; 
🩺, Add or update healthcheck; 
🧱, Infrastructure related changes; 
🧑‍💻, Improve developer experience; 
💸, Add sponsorships or money related infrastructure; 
🧵, Add or update code related to multithreading or concurrency; 
🦺, Add or update code related to validation."""

CONVENTIONAL_COMMIT_KEYWORDS = 'Do not preface the commit with anything, except for the conventional commit keywords: fix, feat, build, chore, ci, docs, style, refactor, perf, test.'

def get_commit_convention(full_git_moji_spec: bool) -> str:
    if global_config['EMOJI']:
        return FULL_GITMOJI_SPEC if full_git_moji_spec else GITMOJI_HELP
    else:
        return CONVENTIONAL_COMMIT_KEYWORDS

description_instruction = 'Add a short description of WHY the changes are done after the commit message. Don\'t start it with "This commit", just describe the changes.' if global_config['DESCRIPTION'] else "Don't add any descriptions to the commit, only commit message."
one_line_commit_guideline = 'Craft a concise commit message that encapsulates all changes made, with an emphasis on the primary updates. If the modifications share a common theme or scope, mention it succinctly; otherwise, leave the scope out to maintain focus. The goal is to provide a clear and unified overview of the changes in a one single message, without diverging into a list of commit per file change.' if global_config['ONE_LINE_COMMIT'] else ''

def init_main_prompt(language: str, full_git_moji_spec: bool) -> dict:
    commit_convention = "GitMoji specification" if full_git_moji_spec else "Conventional Commit Convention"
    mission_statement = (
        f"{IDENTITY} Your mission is to create clean and comprehensive commit messages "
        f"as per the {commit_convention} and explain WHAT were the changes and mainly WHY the changes were done."
    )
    diff_instruction = "I'll send you an output of 'git diff --staged' command, and you are to convert it into a commit message."

    convention_guidelines = get_commit_convention(full_git_moji_spec)
    general_guidelines = (
        f"Use the present tense. Lines must not be longer than 74 characters. "
        f"Use {language} for the commit message."
    )

    content = (
        f"{mission_statement}\n"
        f"{diff_instruction}\n"
        f"{convention_guidelines}\n"
        f"{description_instruction}\n"
        f"{one_line_commit_guideline}\n"
        f"{general_guidelines}"
    )

    return {
        'role': 'system',
        'content': content
    }

INIT_DIFF_PROMPT = {
    "role": "user",
    "content": """diff --git a/src/server.ts b/src/server.ts
    index ad4db42..f3b18a9 100644
    --- a/src/server.ts
    +++ b/src/server.ts
    @@ -10,7 +10,7 @@
    import {
        initWinstonLogger();
        
        const app = express();
        -const port = 7799;
        +const PORT = 7799;
        
        app.use(express.json());
        
        @@ -34,6 +34,6 @@
        app.use((_, res, next) => {
            // ROUTES
            app.use(PROTECTED_ROUTER_URL, protectedRouter);
            
            -app.listen(port, () => {
                -  console.log(\`Server listening on port \${port}\`);
                +app.listen(process.env.PORT || PORT, () => {
                    +  console.log(\`Server listening on port \${PORT}\`);
                });"""
}


def get_content(translation: Language):
    fix = f"🐛 {remove_conventional_commit_word(translation.commitFix)}" if global_config['EMOJI'] else translation.commitFix
    feat = f"✨ {remove_conventional_commit_word(translation.commitFeat)}" if global_config['EMOJI'] else translation.commitFeat
    description = translation.commitDescription if global_config['DESCRIPTION'] else ''
    return f"{fix}\n{feat}\n{description}"

def init_consistency_prompt(translation: Language):
    return {
        "role": "assistant",
        "content": get_content(translation)
    }


def get_main_commit_prompt(full_git_moji_spec: bool):
    return [
        init_main_prompt(translation.localLanguage, full_git_moji_spec),
        INIT_DIFF_PROMPT,
        init_consistency_prompt(translation)
    ]
