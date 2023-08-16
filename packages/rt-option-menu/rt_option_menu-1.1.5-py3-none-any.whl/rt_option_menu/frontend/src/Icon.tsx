import React from 'react';
import * as icons from 'react-bootstrap-icons';

interface IconProps extends icons.IconProps {
  // Cannot use "name" as it is a valid SVG attribute
  // "iconName", "filename", "icon" will do it instead
  iconName: keyof typeof icons;
  size: number;
  style: any;
}

export const Icon = ({ iconName, ...props }: IconProps) => {
  let BootstrapIcon = icons[iconName];
  const iconStyle = { ...props.style };
  if (!BootstrapIcon){
    iconStyle.visibility = 'hidden';
    BootstrapIcon = icons['XCircleFill']
  }
  return <BootstrapIcon size={props.size} style={iconStyle} />;
}