// @ts-nocheck
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Icon } from "./Icon";

interface State {
  selectedChoice: string
}

interface ComponentOptions {
  orientation?: string;
  icons?: string[];
  links?: string[];
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class RtOptionMenu extends StreamlitComponentBase<State> {
  constructor(props: any) {
    super(props);

    if (props.args.default) {
      this.state = { selectedChoice: props.args.default };
    }

  }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const choices: string[] = this.props.args["choices"];
    const options: ComponentOptions = this.props.args["options"] || {};

    const selectedChoice = this.state.selectedChoice;

    if (options.orientation === 'horizontal') {
      const containerStyle = {
        display: 'flex',
        flexDirection: 'row' as 'row',
        alignItems: 'center',
        justifyContent: 'space-evenly',
        columnGap: '0.5em',
        backgroundColor: 'rgb(240,240,240)',
        padding: '0.5em',
        borderRadius: '10px'
      }
      const elementStyle = {
        padding: '0.25em',
        flex: 1,
        background: 'rgb(237,240,244)',
        cursor: 'pointer',
        textAlign: 'center',
        userSelect: 'none' as 'none',
      }
      const selectedElementStyle = {
        ...elementStyle,
        background: 'rgba(107, 101, 255)',
        borderRadius: '10px',
        color: 'white',
      }
      return (
        <div style={containerStyle}>
          {choices.map((choice, index) => {
            return <div key={index} style={selectedChoice === choice ? selectedElementStyle : elementStyle} onClick={() => this.handleChoiceClick(choice)}>{choice}</div>
          })}
        </div>
      )
    }
    // vertical style
    else{
      const containerStyle = {
        display: 'flex',
        flexDirection: 'column' as 'column',
        justifyContent: 'space-evenly',
        alignItems: 'flex-start',
      }
      const elementStyle = {
        display: 'flex',
        flexDirection: 'row' as 'row',
        alignItems: 'flex-start',
        marginTop: '1em',
        width: '100%',
        padding: '0.5em',
        userSelect: 'none' as 'none',
        cursor: 'pointer',
      }
      const selectedElementStyle = {
        ...elementStyle,
        background: 'rgba(107, 101, 255, 0.1)',
        fontWeight: 500
      }
      const leftIconStyle = {
        marginLeft: '0.5em',
        marginRight: '2em',
      }
      const rightIconStyle = {
        marginLeft: 'auto'
      }
      const textStyle = {
        fontSize: '15px',
      }
      const icons = options.icons || [];
      const links = options.links || [];
      return (
        <div style={containerStyle}>
          {choices.map((choice, index) => {
            let leftIcon, rightIcon;
            let link = links[index];

            if (Array.isArray(icons[index])){
              leftIcon = icons[index][0];
              rightIcon = icons[index][1];
            }
            else {
              leftIcon = icons[index];
              rightIcon = undefined;
            }

            if (selectedChoice === choice){
              return <div key={choice} onClick={() => this.handleChoiceClick(choice)} style={selectedElementStyle}><Icon iconName={leftIcon} size={25} style={leftIconStyle}/><span style={textStyle}>{choice}</span><Icon iconName={rightIcon} size={25} style={rightIconStyle}/></div>
            }
            else{
              if (!(link)){
                return <div key={choice}  onClick={() => this.handleChoiceClick(choice)} style={elementStyle}><Icon iconName={leftIcon} size={25} style={leftIconStyle}/><span style={textStyle}>{choice}</span><Icon iconName={rightIcon} size={25} style={rightIconStyle}/></div>
              }
              else{
                return <div key={choice}  onClick={() => this.handleLinkClick(link)} style={elementStyle}><Icon iconName={leftIcon} size={25} style={leftIconStyle}/><span style={textStyle}>{choice}</span><Icon iconName={rightIcon} size={25} style={rightIconStyle}/></div>
              }
            }
          })}
        </div>
      )
    }
  }

  private handleLinkClick = (link: string): void => {
    window.open(link, '_blank');
  }

  private handleChoiceClick = (clickedChoice: string): void => {
    this.setState({ selectedChoice: clickedChoice })

    this.setState(
      prevState => ({selectedChoice: clickedChoice}),
      () => Streamlit.setComponentValue(this.state.selectedChoice)
    )
  }

}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(RtOptionMenu)
