import { compareData, gameData } from "../data_version.js";
import { longClickToFilter } from "../filters.js";
import { StatsEnum, currentSpecieID, feedPanelSpecies, getColorOfStat, getSpritesShinyURL, getSpritesURL } from "../panels/species/species_panel.js";
import { JSHAC, e } from "../utils.js";
import { nodeLists } from "./hydrate.js";


export function toggleLayoutList(toggle = true) {
    if (toggle) {
        // I tried not using hide() but apparently it has not affect on the lag issue
        // No clue on how to fix this besides reworking a completely new loading system where it's generated on scroll
        $('#panel-list-species').css('display', 'flex')
        $('#panel-block-species').css('display', 'none')
    } else {
        $('#species-return-list-layout').hide()
        $('#panel-list-species').css('display', 'none')
        $('#panel-block-species').css('display', 'flex')
    }
}


export function hydrateSpeciesList() {
    const species = gameData.species
    const speciesLen = species.length
    const fragment = document.createDocumentFragment();
    for (let specieID = 0; specieID < speciesLen; specieID++) {
        if (specieID == 0) continue // skip specie none
        const specie = species[specieID]
        const nameRow = e('div', 'list-species-name')
        let imageIsShiny = false
        nameRow.onclick = () => {
            imageIsShiny = !imageIsShiny
            image.src = imageIsShiny ? getSpritesShinyURL(specie.NAME) : getSpritesURL(specie.NAME)

        }
        /*row.setAttribute('draggable', true);
        row.ondragstart = (ev) => {
            ev.dataTransfer.setData("id", i)
        }*/
        //Node id because for correlation with nodelist in sorting
        /*specie.nodeID = nodeLists.species.length
        nodeLists.species.push(row)*/

        const image = e('img', 'species-list-sprite list-species-sprite')
        image.src = getSpritesURL(specie.NAME)
        image.alt = specie.name
        image.loading = "lazy"
        nameRow.appendChild(image)

        const name = e('span', "species-name span-a", specie.name)
        nameRow.append(name)
        const nodeSpecieRow = JSHAC([
            e('div', 'list-species-row'), [
                nameRow,
                e('div', 'list-species-abis-block', [...new Set(specie.stats.abis)].filter(x => x).map(x => {
                    const abiName = gameData.abilities[x].name
                    const abiNode = e('div', 'list-species-abi', [e('span', null, abiName)])
                    longClickToFilter(0, abiNode, "ability", () => { return abiName })
                    return abiNode
                })),
                e('div', 'list-species-inns-block', [...new Set(specie.stats.inns)].filter(x => x).map(x => {
                    const innName = gameData.abilities[x].name
                    const innNode = e('div', 'list-species-inn', [e('span', null, innName)])
                    longClickToFilter(0, innNode, "ability", () => { return innName })
                    return innNode
                })),
                e('div', 'list-species-types-block', [...new Set(specie.stats.types)].map(x => {
                    const type = gameData.typeT[x]
                    const typeNode = e('div', `list-species-type type ${type.toLowerCase()}`, [e('span', null, type)])
                    longClickToFilter(0, typeNode, "type", () => { return type })
                    return typeNode
                })),
                e('div', 'list-species-basestats-block', StatsEnum.concat(["BST"]).map((x, i) => {
                    const statValue = specie.stats.base[i]
                    const color = getColorOfStat(statValue, i)
                    const statNode = e('span', null, statValue)
                    $(statNode).css('background-color', color)
                    const comp = compareData?.species?.[specieID].stats?.base[i]
                    if (comp) {
                        return JSHAC([
                            e('div', 'list-species-basestats-col', [
                                e('div', 'list-species-basestats-head', x),
                                e('div', 'list-species-basestats-val', [
                                    e('span', 'crossed', comp),
                                    e('br', null, '→'),
                                    statNode,
                                ])
                            ])
                        ])
                    } else {
                        return JSHAC([
                            e('div', 'list-species-basestats-col', [
                                e('div', 'list-species-basestats-head', x),
                                e('div', 'list-species-basestats-val', [
                                    statNode,
                                ])
                            ])
                        ])
                    }

                })),
                e('div', 'list-species-btn-view', [e('span', null, 'View')], {
                    onclick: (ev) => {
                        feedPanelSpecies(specieID)
                        toggleLayoutList(false)
                        $('#species-return-list-layout').show()
                    }
                })
            ]
        ])
        nodeLists.listLayoutSpecies.push(nodeSpecieRow.firstChild)
        if (specieID > LIST_RENDER_RANGE) $(nodeSpecieRow.firstChild).hide()
        fragment.append(nodeSpecieRow)
    }
    $('#panel-list-species').empty().append(fragment)
}
export const LIST_RENDER_RANGE = 20

let lastNbScrolled = 0
let unloadOffset = 0
function listRenderingUpdate() {
    const panelDiv = document.getElementById("panel-list-species")
    const oneRowHeightPx = panelDiv.children[lastNbScrolled].clientHeight
    const nbRowScrolled = Math.round(panelDiv.scrollTop / oneRowHeightPx) + unloadOffset
    // first hide those out of range
    const minCurrToRender = Math.max(0, nbRowScrolled - LIST_RENDER_RANGE)
    const maxCurrToRender = Math.min(gameData.species.length - 1, nbRowScrolled + LIST_RENDER_RANGE)
    const minPrevToRender = Math.max(0, lastNbScrolled - LIST_RENDER_RANGE)
    const maxPrevToRender = Math.min(gameData.species.length - 1, lastNbScrolled + LIST_RENDER_RANGE)
    console.log(unloadOffset, nbRowScrolled, minCurrToRender, maxCurrToRender, minPrevToRender, maxPrevToRender)
    if (nbRowScrolled > lastNbScrolled){//scrolled down
        for (let i = minPrevToRender; i < minCurrToRender; i++){
            nodeLists.listLayoutSpecies[i].style.display = "none"
        }
        unloadOffset += minCurrToRender - minPrevToRender
    } else { //scrolled up
        for (let i = maxPrevToRender; i > maxCurrToRender; i--){
            nodeLists.listLayoutSpecies[i].style.display = "none"
        }
        unloadOffset = Math.max(0, unloadOffset - (maxPrevToRender - maxCurrToRender))
    }
    for (let i = minCurrToRender; i < maxCurrToRender; i++){
        nodeLists.listLayoutSpecies[i].style.display = "flex"
    }
    // show those in range
    lastNbScrolled = nbRowScrolled
}

export function setupListSpecies() {
    $('#panel-list-species').on('scrollend', () => {
        fastdom.mutate(() => {
            listRenderingUpdate()
        })
    })
}