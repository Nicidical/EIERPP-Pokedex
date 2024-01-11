import * as FS from 'fs'
import * as Path from 'path'

import {getFileData, getMulFilesData,autojoinFilePath, FileDataOptions} from './utils';
import * as Moves from './moves'
import * as Species from './species/species'
import * as Abilities from './abilities'
import * as Sprites from './sprites'
import { CompactGameData, compactify } from './compactify';

const ROOT_PRJ = "/media/notalinux/_dev_sdb3/Website/reduxelite"



export interface GameData {
    species: Species.Specie[]
    abilities: [string, Abilities.Ability][]
    moves:[string, Moves.Move][]
}

const gameData: GameData = {
    species: [] as Species.Specie[],
    abilities: [],
    moves: [],
}

function main(){
    const OUTPUT_VERSION = process.argv[2] ? "V" + process.argv[2] : ""
    const OUTPUT = `./dist/gameData${OUTPUT_VERSION}.js`


    getFileData(Path.join(ROOT_PRJ, 'include/global.h'))
    .then((global_h) => {
        global_h.data
        const optionsGlobal_h = {
            filterComments: true,
            filterMacros: true,
            macros: global_h.macros
        }
        if (process.argv[2] === "sprites"){
            const OUTPUT_SPRITES = Path.join(__dirname, "sprites/")
            getSprites(optionsGlobal_h, OUTPUT_SPRITES)
                .then(()=>{
                    console.log('Successfully copied the sprites')
                })
                .catch((err)=>{
                    console.error('error while trying to catch sprites ' + err)
                })
        } else {
            const promiseArray: Array<Promise<undefined>> = []
            promiseArray.push(getSpecies(optionsGlobal_h))
            promiseArray.push(getMoves(optionsGlobal_h))
            promiseArray.push(getAbilities(optionsGlobal_h))
            Promise.allSettled(promiseArray)
                .then(()=>{
                    outputGameData(compactify(gameData), OUTPUT)
                })
                .catch((err)=>{
                    console.error(`Something went wrong parsing the data: ${err}`)
                })
        }
        
    })
    .catch((reason) => {
        const err = 'Failed at gettings global.h reason: ' + reason
        console.error(err)
    })
}

function outputGameData(gameData: GameData | CompactGameData, output: string){
    const dataTowrite = "gameData = " + JSON.stringify(gameData) + ";hydrate()"
    FS.writeFile(output, dataTowrite , (err_exist)=>{
        if (err_exist){
            console.error(`couldn't write the gamedata output to ${output}`)
        }
    })
}

function getSpecies(optionsGlobal_h: FileDataOptions){
    return new Promise((resolve: (undefined: undefined)=>void, reject)=>{
        getMulFilesData(autojoinFilePath(ROOT_PRJ, [//'src/data/pokemon/pokedex_entries.h', //will do later
                                                //'src/data/pokemon/pokedex_text.h', //both goes together with entries
                                                'src/data/text/species_names.h',
                                                'src/data/pokemon/base_stats.h',
                                                'src/data/pokemon/evolution.h',
                                                'src/data/pokemon/egg_moves.h',
                                                'src/data/pokemon/level_up_learnsets.h', // order with pointers is important
                                                'src/data/pokemon/level_up_learnset_pointers.h',
                                                'src/data/pokemon/tmhm_learnsets.h',
                                                'src/data/pokemon/tutor_learnsets.h',
                                                'src/data/pokemon/form_species_tables.h',
                                                'src/data/pokemon/form_species_table_pointers.h',
                                                'src/data/graphics/pokemon.h',
                                                'src/data/pokemon_graphics/front_pic_table.h',
                                            ]), optionsGlobal_h)
        .then((pokeData)=>{
            gameData.species = Species.parse(pokeData)
            resolve(null)
        })
        .catch((reason)=>{
            const err = 'Failed at gettings species reason: ' + reason
            reject(err)
        })
    })
    
}

function getMoves(optionsGlobal_h: FileDataOptions){
    return new Promise((resolve: (undefined: undefined)=>void, reject)=>{
        getFileData(Path.join(ROOT_PRJ, 'include/constants/battle_config.h'), optionsGlobal_h)
                .then((battle_config) => {
                    const optionsBattle = {
                        filterComments: true,
                        filterMacros: true,
                        macros: battle_config.macros
                    }
                    getMulFilesData(autojoinFilePath(ROOT_PRJ, ['src/data/battle_moves.h', 
                                                                'src/data/text/move_descriptions.h',
                                                                'src/data/text/move_names.h'] ), optionsBattle)
                        .then((movesData)=>{
                            gameData.moves = Moves.parse(movesData)
                            resolve(null)
                        })
                        .catch(reject)
                        
                })
                .catch(reject)
    })
  
}

function getAbilities(optionsGlobal_h: FileDataOptions){
    return new Promise((resolve: (undefined: undefined)=>void, reject)=>{
        getMulFilesData(autojoinFilePath(ROOT_PRJ, ['src/data/text/abilities.h',
                                                ]), optionsGlobal_h)
            .then((abilityData)=>{
                gameData.abilities = Abilities.parse(abilityData)
                resolve(null)
            })
            .catch((reason)=>{
                const err = 'Failed at gettings species reason: ' + reason
                reject(err)
            })
    })
    
}

function getSprites(optionsGlobal_h: FileDataOptions, output_dir: string){
    return new Promise((resolve: (undefined: undefined)=>void, reject)=>{
        if (!FS.existsSync(output_dir)) {
            try {
                FS.mkdirSync(output_dir)
            } catch{
                reject(`Failed to create output directory for sprites : ${output_dir}`)
            }
        }
        getMulFilesData(autojoinFilePath(ROOT_PRJ, ['src/data/graphics/pokemon.h',
                                                'src/data/pokemon_graphics/front_pic_table.h',
                                            ]), optionsGlobal_h)
        .then((spriteData)=>{
            const lines = spriteData.split('\n')
            const spriteResult = Sprites.parse(lines, 0)
            
            spriteResult.spritesPath.forEach((val, key)=>{
                const inFilePath =Path.join(ROOT_PRJ, val)
                const outFileName = key.replace(/^SPECIES_/, '') + ".png"
                const outFilePath = Path.join(output_dir, outFileName)
                try{
                    if (FS.existsSync(inFilePath)){
                        FS.copyFileSync(inFilePath, outFilePath)
                    } else {
                        throw `${inFilePath} does not exist`
                    }
                    
                } catch(e){
                    console.warn(`Tried to copy ${inFilePath} to ${outFilePath} error: ${e}`)
                }
                
            })
            resolve(null)
        })
        .catch((reason)=>{
            const err = 'Failed at gettings species reason: ' + reason
            reject(err)
        })
    })
    
}


main()