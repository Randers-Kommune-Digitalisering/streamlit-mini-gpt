# Streamlit Mini-GPT `README.md`
[**Formål**](#formål) | [**Beskrivelse**](#beskrivelse) | [**Afhængigheder**](#afh%C3%A6ngigheder) | [**Deployment**](#deployment)

## Formål

Formålet med applikationen er at udstille en vilkårlig Azure OpenAI-assistent gennem et Streamlit-webinterface, og give brugerene mulighed for at uploade eller fjerne filer fra assistentens vektordatabase.

## Beskrivelse

Webapplikationen er bygget med Streamlit og består af to hovedfunktioner: et chat-interface til interaktion med Azure OpenAI-assistenten og et filhåndterings-interface til administration af assistentens vektordatabase.

**Dataflow for chat:**
- Når en bruger sender en besked, oprettes en ny tråd via Azure OpenAI's REST API.
- Alle beskeder i sessionen sendes til API'et, og assistentens svar hentes asynkront, indtil svaret er klar.
- Eventuelle referencer til filer i svaret mappes til filnavne, så brugeren kan se hvilke kilder, der er anvendt.
- Svar og eventuelle fodnoter vises i chatten, og brugeren kan kopiere svaret direkte.

**Dataflow for filhåndtering:**
- Brugeren kan uploade filer, som sendes til Azure OpenAI via API'et og gemmes i assistentens vektordatabase.
- Filer kan herefter tilføjes eller fjernes fra den valgte vector store, hvilket opdaterer assistentens videnbase dynamisk.
- Alle filoperationer (upload, tilføj, slet) håndteres via dedikerede API-kald, og status vises løbende i UI'et.

**Session og tilstand:**
- Applikationen benytter Streamlit session state til at holde styr på beskeder, tilgængelige filer og vektor store-indhold på tværs af brugerens session.
- Miljøvariabler styrer endpoints, credentials og konfiguration, så løsningen let kan tilpasses forskellige miljøer.

**Sikkerhed og integration:**
- API-nøgler og endpoints håndteres via miljøvariabler og bør sikres i deployment-miljøet.
- Løsningen kan integreres med KeyCloak/OpenID for adgangsstyring, hvis ønsket.

Denne arkitektur sikrer, at både chat og filhåndtering er tæt integreret med Azure OpenAI, og at brugeren altid arbejder med opdateret viden og sikre dataflows.

## Afhængigheder

:gear: | **Frameworks, komponenter og moduler**
- Python 3.10+
- Streamlit (webframework til frontend og interaktivitet)
- Requests (HTTP-klient til API-kald)

Installér afhængigheder med:

```bash
pip install -r src/requirements.txt
```

:cloud: | **API'er, CDN'er og andre online services**
- Azure OpenAI (kræver adgang til Azure OpenAI-tjenester)

:key: | **Miljøvariabler**

- `ASSISTANT_NAME` Assistentens navn som vises i applikationen (default: assistenten).

- `ASSISTANT_ID` Assistentens ID i Azure OpenAI.

- `VECTOR_STORE_ID` Assistentens vector store ID i Azure OpenAI.

- `PREDEFINED_QUESTIONS` Foruddefinerede spørgsmål som vises i applikationen. Flere spørgsmål opdeles med semikolon, f.eks "*Spørgsmål 1;Spørgsmål 2*" (default: Hvad kan du hjælpe mig med?).

- `AZURE_OPENAI_ENDPOINT` URL til Azure OpenAI.

- `AZURE_OPENAI_KEY` API nøgle til Azure OpenAI.

- `AZURE_API_VERSION` API version (default: 2024-05-01-preview)

- `AZURE_API_VERSION_FILES` API version til filhåndtering (default: 2024-10-21)

- `AZURE_API_VERSION_VECTORS` API version til vektorhåndtering (default: 2025-03-01-preview)


- `DEBUG` Til yderligere backend debugging (True/False).

- `PORT` Applikationens port (standard: 8080)

- `POD_NAME` Applikationens pod name (K8)


## Deployment

Løsningen er designet til at blive deployet på Kubernetes (K8s) ved hjælp af Helm charts. Følg nedenstående trin for at deploye applikationen på Randers Kommunes miljø:

1. **Opret assistent samt vector store i Azure OpenAI:**

   - Tilgå Azure OpenAI, og opret en ny assistent samt en dertilhørende vector store.
   - Aktiver 'File search' for assistenten, og vælg den tilhørende vector store.
   - Noter ID på både assistenten og vector store.

2. **Vælg version:**

   - Find image bygget fra dette repository (se **[Packages](https://github.com/orgs/Randers-Kommune-Digitalisering/packages?repo_name=streamlit-mini-gpt)**).
   - Noter den ønskede versions tag (eller full SHA).

3. **KeyCloak:**
   - Opret en ny klient i KeyCloak med et beskrivende navn.
   - Slå *Client authentication* til på klienten.
   - Tilføj `groups` til *Client scopes* på klienten, såfremt gruppebaseret adgangsstyring ønskes.
   - Noter `clientSecret` og generér en `cookieSecret` ud fra OpenID dokumentation.

4. **Konfigurér:**
   - Opret `values.yaml` + `values-prod.yaml`
   - Tilpas værdier i `values.yaml` (version-tag, miljøvariabler, samt open-id konfiguration).
   - Tilpas værdier i `values-test.yaml` (hosts værdier samt open-id secrets)


5. **Sync på Argo**
   - Du har nu idriftsat en ny mini-GPT :)
