import pandas as pd
import pokebase as pb
import numpy as np

def get_info(id):
    
    pokemon = pb.pokemon(id)
    
    order = id
    
    name = pokemon.name
    
    height = pokemon.height
    
    weight = pokemon.weight
    
    base_exp = pokemon.base_experience
    
    stats = pokemon.stats
    
    hp = stats[0].base_stat
    
    atk = stats[1].base_stat
    
    defense = stats[2].base_stat
    
    spatk = stats[3].base_stat
    
    spdef = stats[4].base_stat
    
    speed = stats[5].base_stat
    
    ptype = str(pokemon.types[0].type)
    
    stype = str(pokemon.types[-1].type)
    
    try:
        evolution = pb.evolution_chain(id).chain.evolves_to[0].species.name
    except:
        evolution = np.NaN
    
    if stype == ptype:
        stype = np.NaN
        
    info = {
        "id": order,
        "name": name,
        "height": height,
        "weight": weight,
        "base-experience": base_exp,
        "hp": hp,
        "attack": atk,
        "defense": defense,
        "special-attack": spatk,
        "special-defense": spdef,
        "speed": speed,
        "primary-type": ptype,
        "secondary-type": stype,
    }
    
    return info

def create_info_dataframe():
        
    df = pd.DataFrame(columns=['id', 'name', 'height', 'weight', 'base-eperience', 'hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed', 'primary-type', 'secondary-type'])
    
    for i in range(1010):
        df.loc[i] = get_info(i+1)
        
    df['name'] = df['name'].str.title()
    
    return df
    
def get_evolutions(id):
        
    try:
        evolution_chain = pb.evolution_chain(id).chain
    except:
        return
    
    current = str(evolution_chain.species)
    
    evolutions = {}
    
    if evolution_chain.evolves_to:
        while evolution_chain.evolves_to:
            evos = [str(e.species) for e in evolution_chain.evolves_to]
            next_evo = evolution_chain.evolves_to[0]
            for evo in evos:
                evolutions[evo] = current
            current = str(next_evo.species)
            evolution_chain = next_evo
    else:
        evolutions[current] = np.NaN
        
    return evolutions

def get_evo_dataframe():
    
    i = 1
    frames = []
    for i in range(539):
        evo_df = pd.DataFrame(columns=['name', 'evolves-from'])
        evo = get_evolutions(i)
        if evo is None:
            continue
        evo_df['name'] = evo.keys()
        evo_df['evolves-from'] = evo.values()
        frames.append(evo_df)
        i += 1
        
    df = pd.concat(frames).reset_index().drop(columns='index')