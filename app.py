import gradio as gr
from sidekick import Sidekick


async def  setup():
    sidekick = Sidekick()
    await sidekick.setup()
    return sidekick


async def procces_message(sidekick, message, succes_criteria, history):
    results = await sidekick.run_superstep(message, succes_criteria, history)
    return results, sidekick


async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return new_sidekick

def free_resourses(sidekick):
    print("Cleaning up")
    try:
        if sidekick:
            sidekick.free_resourses()
    except Exception as e:
        print(e)


with gr.Block(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Sidekick Personal Co-Worker")

    sidekick = gr.State(delete_callback=free_resourses)

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick", height=300, type="message")

    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="Your request to the Sidekick")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="What are your success critiera?"
            )

        with gr.Row():
            reset_button =gr.Button("Reset", variant="stop")
            go_button = gr.Button("Go", variant="primary")

        ui.load(setup, [], [sidekick])

        message.submit(procces_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])

        success_criteria.submit(procces_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])

        go_button.click(procces_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick])

        reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])

ui.launch(inbrowser=True)
