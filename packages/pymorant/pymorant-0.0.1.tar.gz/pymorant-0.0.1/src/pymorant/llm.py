# import os
import re
import ast
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


def corregir_texto(text, model, openai_key):

    """
    Regresa el texto corregido ortográficamente, utilizando el modelo de
    lenguaje especificado.

    Parametros:
    text (str): texto original
    model (str): modelo de lenguaje a utilizar
    openai_key (str): llave de OpenAI
    """

    if text == "":
        return ""

    pattern = r'^[\'"]|[\'"](?=\.)|[\'"]$'

    prompt = PromptTemplate(

        input_variables=["text"],
        template='''
        Corrige las faltas ortográficas del siguiente texto: '{text}'.
        Si no encuentras faltas ortográficas, simplemente déjalo como está,
        sin hacer cambios. No menciones si el texto no tiene errores
        ortográficos, solo agrégalo tal y como estaba.
        '''
    )

    chatopenai = ChatOpenAI(model_name=model, openai_api_key=openai_key)
    llmchain_chat = LLMChain(llm=chatopenai, prompt=prompt)

    corrected_text = llmchain_chat.run(text)
    cleaned_text = re.sub(pattern, '', corrected_text)

    return cleaned_text


def generar_variantes_texto(text, n, model, openai_key, formal=False, sex="NA"): # noqa
    '''
    Regresa una lista de n variantes del texto original, utilizando el modelo
    de lenguaje especificado. Si formal=True, se generan variantes formales.

    Parametros:
    text (str): texto original
    n (int): número de variantes a generar
    model (str): modelo de lenguaje a utilizar
    openai_key (str): llave de OpenAI
    formal (bool): si True, se generan variantes formales
    sex: sexo de la persona a la que se dirige el texto.
    Puede ser "H" (hombre), "M" (mujer) o "NA" (no aplica).
    '''

    if text == "" or sex not in ["H", "M", "NA"]:
        print("No se generaron variantes del texto por falta de información correcta") # noqa
        return []

    output_parser = CommaSeparatedListOutputParser()

    format_instructions = output_parser.get_format_instructions()

    if formal:

        template_string = '''
            Eres un experto en análisis de texto. Imagina que recibes el
            siguiente texto: {text_input}. Tu tarea es crear {n_input}
            variaciones únicas de este texto, utilizando diferentes palabras y
            estructuras para transmitir el mismo significado. No puedes
            utilizar palabras que se puedan considerar ofensivas o sexuales.
            Por ejemplo, no utilizar la palabra "estimulante". Además de esto,
            considera cada variación únicamente para el sexo {sex_input} donde
            H es hombre, M es mujer y NA es que no consideraras el sexo de
            la persona. Por ejemplo, si el sexo es H: puedes escribir algo
            como: "Hola amigo!", "Hola compañero", "Hola colega", etc. Si
            el sexo es M: puedes escribir algo como "Hola amiga!",
            "Hola compañera", "Hola colega", etc. Y si el sexo es "NA", puedes
            escribir algo como "Hola, ¿cómo estás?", "Hola, ¿qué tal?", "Hola,
            ¿qué onda?", etc. Recuerda que debes crear {n_input} variaciones
            únicas del texto. No puedes repetir el mismo texto. RECUERDA
            que TODAS las variaciones generadas son para el sexo {sex_input}
            \n\n{format_instructions}
            '''

    else:

        template_string = '''
            Eres un experto en análisis de texto. Imagina que recibes el
            siguiente texto: {text_input}. Tu tarea es crear {n_input}
            variaciones únicas de este texto, utilizando diferentes palabras
            y estructuras para transmitir el mismo significado. Debes de
            utilizar un lenguaje formal. No puedes utilizar palabras que
            se puedan considerar ofensivas o sexuales. Por ejemplo, no
            utilizar la palabra "estimulante". Además de esto, considera
            cada variación únicamente para el sexo {sex_input} donde H es
            hombre, M es mujer y NA es que no consideraras el sexo de la
            persona. Por ejemplo, si el sexo es H: puedes escribir algo como:
            "Buen día estimado!", "Saludos cordiales", "Buen día apreciado",
            "Buen día respetable", etc. Si el sexo es M: puedes escribir algo
            como "Buen día estimada", "Saludos cordiales", "Esperando te
            encuentres muy bien", "Buen día apreciada", etc. Y si el sexo es
            "NA", puedes escribir algo como "Excelente día", "Espléndido día",
            "Espero estes pasando un día magnífico", etc. Recuerda que debes
            crear {n_input} variaciones únicas del texto. No puedes repetir
            el mismo texto. RECUERDA que TODAS las variaciones generadas
            son para el sexo {sex_input}.
            \n\n{format_instructions}
            '''

    prompt = ChatPromptTemplate(
        messages=[HumanMessagePromptTemplate.from_template(template_string)],
        input_variables=["text_input", "n_input", "sex_input"],
        partial_variables={'format_instructions': format_instructions})

    list_prompt = prompt.format_messages(
        text_input=text,
        n_input=n,
        sex_input=sex,
        format_instructions=format_instructions)

    llm = ChatOpenAI(
        temperature=0.6, openai_api_key=openai_key, model=model)

    output = llm(list_prompt)
    final_list = output.content.split('\n\n')
    pattern = r'^[\'"]|[\'"](?=\.)|[\'"]$'
    final_list = [re.sub(pattern, '', s) for s in final_list]

    return final_list


def resumir_texto(text, model, openai_key, input_autogenerado):

    """
    Regresa un resumen del texto original, utilizando el modelo de lenguaje
    especificado.

    Parametros:
    text (str): texto original
    model (str): modelo de lenguaje a utilizar
    openai_key (str): llave de OpenAI
    input_autogenerado (bool): si True, si el input es auto-generado por
    el modelo previamente.
    """

    llm = OpenAI(temperature=0.0, openai_api_key=openai_key)
    num_tokens = llm.get_num_tokens(text)

    if num_tokens >= 3500:
        raise ValueError("El número de tokens excede lo permitido por el \
            chatbot. Por favor reduce el tamaño de las observaciones a \
            ingresar.")

    if input_autogenerado:

        prompt_template = """
        Eres el mejor analista de texto. Evalúa los criterios necesarios para
        crear un buen resumen utilizando esta información: {text}
        """

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["text"]
        )
        prompt = prompt.format(text=text)
        respuesta = llm(prompt)

    else:

        prompt_template = """
        Eres el mejor analista de texto. Evalúa los criterios necesarios para
        crear un buen resumen utilizando esta información: {text}
        """

        docs = [Document(page_content=t) for t in text]

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["text"]
        )

        chain = load_summarize_chain(
            llm=llm, chain_type='stuff', prompt=prompt
        )

        respuesta = chain.run(docs)

    return respuesta


def generar_categorias(text, n, model, openai_key):

    """
    Regresa una lista de n categorías del texto original, utilizando el modelo
    de lenguaje especificado.

    Parametros:
    text (str): texto original
    n (int): número de categorías a generar
    model (str): modelo de lenguaje a utilizar
    openai_key (str): llave de OpenAI
    """

    try:
        prompt = PromptTemplate(
            input_variables=["lista", "n_input"],
            template='''Recibí un resumen con características clave de las
            respuestas auna pregunta: '{lista}'. A partir de esta información,
            genera {n_input} categorías que representen los aspectos más
            relevantes. No expliques a que se refiere cada categoría.
            Devuelve estas categorías en una lista de Python lista para poder
            ser procesada.'''
        )

        chatopenai = ChatOpenAI(
            model_name=model, openai_api_key=openai_key
        )

        llmchain_chat = LLMChain(llm=chatopenai, prompt=prompt)

        categorias = llmchain_chat.run({
            "lista": text,
            "n_input": n,
        })

        categorias_list = ast.literal_eval(categorias)

        return categorias_list
    except Exception as e:
        raise ValueError("Error al generar categorías: " + str(e))
