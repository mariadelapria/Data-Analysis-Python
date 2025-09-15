from sqlalchemy import create_engine
import pandas as pd
from config_db import usuario, senha, host, banco 

# Criar engine
engine = create_engine(f"mysql+pymysql://{usuario}:{senha}@{host}/{banco}")
# Ler a tabela direto no pandas
df = pd.read_sql("SELECT * FROM global_finance_data", engine)

############ Indicadores macroeconômicos ############ 

############ Indicador de PIB


#Média Global do PIB
def media_global(projeto_1,pib_crescimento="pib_crescimento"):
    return projeto_1[pib_crescimento].mean()
print("Média global do PIB:", media_global(df))


# Função para calcular média global e por região
def media_pib_por_regiao(projeto_1, pib_crescimento="pib_crescimento", regiao_nome="regiao_nome"):
    media_global = projeto_1[pib_crescimento].mean()
    media_regiao = df.groupby(regiao_nome)[pib_crescimento].mean()
    return media_global, media_regiao
media_global, media_regiao = media_pib_por_regiao(df)

print("Média porcentagem global do PIB:", media_global)
print("\nMédia do PIB por região:")
print(media_regiao)


#% do PIB por regiao em comparação ao global
def percentual_crescimento_por_regiao(df, pib_col="pib_crescimento", regiao_col="regiao_nome"):
    media_global, media_regiao = media_pib_por_regiao(df, pib_col, regiao_col)
    percentual = (media_regiao / media_global) * 100  
    
    resultado = pd.DataFrame({
        "media_regiao": media_regiao.round(2),
        "percentual_relativo": percentual.round(2)  
    })
    
    resultado["media_regiao"] = resultado["media_regiao"].map("{:.2f}%".format)
    resultado["percentual_relativo"] = resultado["percentual_relativo"].map("{:.2f}%".format)

    return resultado

crescimento_percentual = percentual_crescimento_por_regiao(df)
print(crescimento_percentual)


#Ranking global por região usando a porcentagem calculada
ranking_regiao = percentual_crescimento_por_regiao(df).sort_values("percentual_relativo", ascending=False)
print("Ranking do PIB por região (percentual relativo ao global):")
print(ranking_regiao)

#Ranking de países dentro de cada região pelo crescimento
ranking_pais_por_regiao = df.groupby(["regiao_nome", "pais"])["pib_crescimento"].mean().sort_values(ascending=False)
ranking_pais_por_regiao = ranking_pais_por_regiao.reset_index()
print("\nRanking de países por região (crescimento do PIB):")
print(ranking_pais_por_regiao)


############ Indicador de Inflação


#Média Global da Inflação
def media_global_inflacao(df,inflacao="inflacao"):
    return df[inflacao].mean()
print("Média global de Inflação:", media_global_inflacao(df))


# Função para calcular média de Inflação global e por região
def media_inflacao_por_regiao(projeto_1, inflacao="inflacao", regiao_nome="regiao_nome"):
    media_global = df[inflacao].mean()
    media_regiao = df.groupby(regiao_nome)[inflacao].mean()
    return media_global, media_regiao
media_global, media_regiao = media_inflacao_por_regiao(df)

print("Média porcentagem global de Inflação", media_global)
print("\nMédia do Inflação por região:")
print(media_regiao)


#% da Inflação por regiao em comparação ao global
def percentual_inflacao_por_regiao(df, inflacao="inflacao", regiao_nome="regiao_nome"):
    media_global, media_regiao = media_inflacao_por_regiao(df, inflacao, regiao_nome)
    percentual = (media_regiao / media_global) * 100  
    
    resultado = pd.DataFrame({
        "media_regiao": media_regiao.round(2),
        "percentual_relativo": percentual.round(2)  
    })
    
    resultado["percentual_relativo_num"] = percentual
    resultado["media_regiao"] = resultado["media_regiao"].map("{:.2f}%".format)
    resultado["percentual_relativo"] = resultado["percentual_relativo"].map("{:.2f}%".format)

    return resultado

crescimento_percentual = percentual_inflacao_por_regiao(df)
print(crescimento_percentual)


#Ranking global de Inflação por região usando a porcentagem calculada
ranking_regiao = percentual_inflacao_por_regiao(df).sort_values("percentual_relativo", ascending=False)
print("Ranking de Inflação por região (percentual relativo ao global):")
print(ranking_regiao)

#Ranking de Inflação de países dentro de cada região pelo crescimento
ranking_pais_por_regiao = df.groupby(["regiao_nome", "pais"])["inflacao"].mean().sort_values(ascending=False)
ranking_pais_por_regiao = ranking_pais_por_regiao.reset_index()
print("\nRanking de países por região (Inflação Média):")
print(ranking_pais_por_regiao)


#Classificação de risco
def classificar_inflacao(df, inflacao="inflacao"):
    """
    - Baixo: até 3%
    - Moderado: >3% até 6%
    - Alto: >6%
    """
    def risco(valor):
        if valor <= 3:
            return "Baixo"
        elif valor <= 6:
            return "Moderado"
        else:
            return "Alto"
    df["classificacao_risco"] = df[inflacao].apply(risco)
    return df
df = classificar_inflacao(df)
print(df[["pais", "regiao_nome", "inflacao", "classificacao_risco"]])


############ Indicador de Taxa de Juros

#Média Global da Taxa de Juros
def media_global_juros(df,taxa_juros="taxa_juros_pct"):
    return df[taxa_juros].mean()
print("Média global de Taxa de Juros:", media_global_juros(df))


# Função para calcular média de Juros global e por região
def media_juros_por_regiao(projeto_1,taxa_juros="taxa_juros_pct", regiao_nome="regiao_nome"):
    media_global = df[taxa_juros].mean()
    media_regiao = df.groupby(regiao_nome)[taxa_juros].mean()
    return media_global, media_regiao
media_global, media_regiao = media_juros_por_regiao(df)

print("Média porcentagem global de Juros", media_global)
print("\nMédia do Juros por região:")
print(media_regiao)


#% da Taxa de Juros por regiao em comparação ao global
def percentual_juros_por_regiao(df,taxa_juros="taxa_juros_pct", regiao_nome="regiao_nome"):
    media_global, media_regiao = media_juros_por_regiao(df, taxa_juros, regiao_nome)
    percentual = (media_regiao / media_global) * 100  
    
    resultado = pd.DataFrame({
        "media_regiao": media_regiao.round(2),
        "percentual_relativo": percentual.round(2)  
    })
    
    resultado["percentual_relativo_num"] = percentual
    resultado["media_regiao"] = resultado["media_regiao"].map("{:.2f}%".format)
    resultado["percentual_relativo"] = resultado["percentual_relativo"].map("{:.2f}%".format)

    return resultado

percentual_juros = percentual_juros_por_regiao(df)
print(percentual_juros)


#Ranking global de Juros por região usando a porcentagem calculada
ranking_regiao = percentual_juros_por_regiao(df).sort_values("percentual_relativo", ascending=False)
print("Ranking de Taxa de Juros por região (percentual relativo ao global):")
print(ranking_regiao)

#Ranking de Juros de países dentro de cada região pelo crescimento
ranking_pais_por_regiao = df.groupby(["regiao_nome", "pais"])["taxa_juros_pct"].mean().sort_values(ascending=False)
ranking_pais_por_regiao = ranking_pais_por_regiao.reset_index()
print("\nRanking de países por região (Taxa de Juros Média):")
print(ranking_pais_por_regiao)


############ Indicador de Cambio (nível absoluto)


#Média Global da Cambio (nível absoluto)
def media_global_cambio_abs(df,cambio="cambio_usd"):
    return df[cambio].mean()
print("Média global de Cambio (nível absoluto):", media_global_cambio_abs(df))


# Função para calcular média Cambio (nível absoluto) global e por região
def media_cambio_abs_por_regiao(projeto_1,cambio="cambio_usd", regiao_nome="regiao_nome"):
    media_global = df[cambio].mean()
    media_regiao = df.groupby(regiao_nome)[cambio].mean()
    return media_global, media_regiao
media_global, media_regiao =media_cambio_abs_por_regiao(df)

print("Média porcentagem global de Cambio ABS", media_global)
print("\nMédia do Cambio ABS por região:")
print(media_regiao)


#% da Taxa de Cambio (nível absoluto) por regiao em comparação ao global
def percentual_cambio_abs_por_regiao(df,cambio="cambio_usd", regiao_nome="regiao_nome"):
    media_global, media_regiao = media_cambio_abs_por_regiao(df, cambio, regiao_nome)
    percentual = (media_regiao / media_global) * 100  
    
    resultado = pd.DataFrame({
        "media_regiao": media_regiao.round(2),
        "percentual_relativo": percentual.round(2)  
    })
    
    resultado["percentual_relativo_num"] = percentual
    resultado["percentual_relativo"] = resultado["percentual_relativo"].map("{:.2f}%".format)

    return resultado

percentual_cambio_abs = percentual_cambio_abs_por_regiao(df)
print(percentual_cambio_abs)


#Ranking global de Cambio (nível absoluto) por região usando a porcentagem calculada
ranking_regiao = percentual_cambio_abs_por_regiao(df).sort_values("percentual_relativo", ascending=False)
print("Ranking de Cambio ABS por região (percentual relativo ao global):")
print(ranking_regiao)

#Ranking de Cambio (nível absoluto) de países dentro de cada região 
ranking_pais_por_regiao = df.groupby(["regiao_nome", "pais"])["cambio_usd"].mean().sort_values(ascending=False)
ranking_pais_por_regiao = ranking_pais_por_regiao.reset_index()
print("\nRanking de países por região (Cambio ABS Médio):")
print(ranking_pais_por_regiao)


############ Indicador de Cambio (Variação Anual)


#Média Global da Cambio (Variação Anual)
def media_global_cambio_var(df,cambio_var="cambio_ano"):
    return df[cambio_var].mean()
print("Média global de Cambio (Variação Anual):", media_global_cambio_var(df))


# Função para calcular média Cambio (Variação Anual) global e por região
def media_cambio_var_regiao(projeto_1,cambio_var="cambio_ano", regiao_nome="regiao_nome"):
    media_global = df[cambio_var].mean()
    media_regiao = df.groupby(regiao_nome)[cambio_var].mean()
    return media_global, media_regiao
media_global, media_regiao =media_cambio_var_regiao(df)

print("Média porcentagem global de Cambio (Variação Anual) ", media_global)
print("\nMédia do Cambio (Variação Anual) por região:")
print(media_regiao)


#% da Taxa de Cambio (Variação Anual) por regiao em comparação ao global
def percentual_cambio_var_por_regiao(df,cambio_var="cambio_ano", regiao_nome="regiao_nome"):
    media_global, media_regiao = media_cambio_var_regiao(df, cambio_var, regiao_nome)
    percentual = (media_regiao / media_global) * 100  
    
    resultado = pd.DataFrame({
        "media_regiao": media_regiao.round(2),
        "percentual_relativo": percentual.round(2)  
    })
    
    resultado["percentual_relativo_num"] = percentual
    resultado["percentual_relativo"] = resultado["percentual_relativo"].map("{:.2f}%".format)

    return resultado

percentual_cambio_variavel = percentual_cambio_var_por_regiao(df)
print(percentual_cambio_variavel)


#Ranking global de Cambio (Variação Anual) por região usando a porcentagem calculada
ranking_regiao = percentual_cambio_var_por_regiao(df).sort_values("percentual_relativo", ascending=False)
print("Ranking de Cambio (Variação Anual) por região (percentual relativo ao global):")
print(ranking_regiao)

#Ranking de Cambio (Variação Anual) de países dentro de cada região 
ranking_pais_por_regiao = df.groupby(["regiao_nome", "pais"])["cambio_ano"].mean().sort_values(ascending=False)
ranking_pais_por_regiao = ranking_pais_por_regiao.reset_index()
print("\nRanking de países por região (Cambio Variação Anual Médio):")
print(ranking_pais_por_regiao)







